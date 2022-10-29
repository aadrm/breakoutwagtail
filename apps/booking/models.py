import traceback
from random import randint
from decimal import Decimal
from datetime import datetime, timedelta, time, date

from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django.utils import timezone
from django.utils.timezone import make_aware, is_aware
from django.db import models, transaction
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from breakout.utils import get_booking_settings, textify

from weasyprint import HTML, CSS
# from phonenumber_field.modelfields import PhoneNumberField

from breakout.utils import addmins


# Create your models here

class Invoice(models.Model):

    full_name = models.CharField(_("Name"), max_length=32)
    phone = models.CharField(_("Phone"), max_length=32)
    email = models.EmailField(_("Email"), max_length=128)
    street = models.CharField(_("Street"), max_length=128, blank=True, null=True)
    post = models.CharField(_("Post code"), max_length=8, blank=True, null=True)
    city = models.CharField(_("City"), max_length=32, blank=True, null=True)
    company = models.CharField(_("Company name"), max_length=64, blank=True, null=True)
    payment = models.ForeignKey("booking.PaymentMethod", verbose_name=_("Payment Method"), on_delete=models.PROTECT) 
    is_terms = models.BooleanField(_("Accept terms"), default=False)
    is_privacy = models.BooleanField(_("Accept privacy"), default=False)
    order_date = models.DateTimeField(_("Order Placed"), auto_now=False, auto_now_add=False, blank=True, null=True, editable=False)
    order_int = models.SmallIntegerField(_("Order Number"), blank=True, null=True, editable=False)
    order_number = models.CharField(_("Order Number"), max_length=8, blank=True, null=True, editable=False) 

    def amount_paid(self):
        amount = 0
        for payment in self.payments.all():
            amount += payment.amount
        return amount

    def amount_due(self):
        return self.amount_to_pay() - self.amount_paid()
    
    def amount_to_pay(self):
        try:
            return self.cart.total
        except Exception:
            return 0

    def is_paid(self):
        if self.amount_paid() >= self.amount_to_pay():
            return True
        else:
            return False
    
    @property
    def is_due(self):
        try:
            appointments = self.cart.get_appointment_items()
            if appointments:
                for item in appointments:
                    if item.slot.start.date() < date.today():
                        return True
        except:
            return False
        return False 

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        object_string = str(self.order_number)
        object_string += str(self.full_name)

        return object_string

    def order_next_int(self):
        year = datetime.now().year
        month = datetime.now().month
        orders_inmonth = Invoice.objects.filter(order_date__year=year).filter(order_date__month=month).filter(order_int__isnull=False)

        if not orders_inmonth:
            return 1

        last_order = orders_inmonth.order_by('order_int').last()
        return last_order.order_int + 1

    def create_order_number(self):
        slug = ''
        if self.order_date:
            slug += self.order_date.strftime('%y%W')
        slug += str(randint(1,9)) + str(randint(1,9))
        if self.order_int:
            slug += str(self.order_int).zfill(2)
        return slug

    def get_absolute_url(self):
        return reverse("Invoice_detail", kwargs={"pk": self.pk})

    def commit_order(self):
        """
        Records the current datetime as the order date as well as designating an order number
        """
        if not self.order_date:
            self.order_date = datetime.now()
        if not self.order_number:
            self.order_int = self.order_next_int()
            self.order_number = self.create_order_number()
        self.save()


class Payment(models.Model):
    invoice = models.ForeignKey("booking.Invoice", related_name=('payments'), on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class PaymentMethod(models.Model):

    name = models.CharField(_("display name"), max_length=32)    
    method = models.CharField(_("method"), max_length=16)

    class Meta:
        verbose_name = _("PaymentMethod")
        verbose_name_plural = _("PaymentMethods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PaymentMethod_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    """An item that can be added to the cart using the model cart item"""
    name = models.CharField(_("Product"), max_length=32)    
    price = models.DecimalField(_("Price"), max_digits=8, decimal_places=2)
    upgrade_price = models.DecimalField(_("Upgrade Price"), max_digits=8, decimal_places=2, default=120.00)
    value = models.DecimalField(_("Value"), max_digits=8, decimal_places=2, default=0)
    family = models.ForeignKey("booking.ProductFamily", verbose_name=_("Family"), related_name='products', on_delete=models.CASCADE, null=True, blank=False)
    players = models.SmallIntegerField(_("Players"), blank=True, null=True)
    is_selectable = models.BooleanField(_("Is selectable in calendar"), default=True)

    class Meta:
        ordering = ['price']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        name_str = ''
        name_str += self.players_str()
        name_str += ' | ' + self.family.__str__() 
        return name_str

    def player_price_str(self):
        player_price_str = ''
        player_price_str += self.players_str()
        player_price_str += ' | €' + str(self.price)
        return player_price_str

        

    def players_str(self):
        players_str = ''
        if self.players:
            players_str += str(self.players)
            players_str += ' ' 
            if self.players > 1:
                players_str += _('Players')
            else:
                players_str += _('Player')
        return players_str

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class ProductFamily(models.Model):
    """
    The purpose of this class is to provide a way to group products into families.

    Grouping products make possible to bind several products to a single slot in the calendar,
    allowing the user to choose from several producs for a single appointment.
    Also an interface for including or excluding several products to each of the coupons.
    """
    name = models.CharField(_("Product Family"), max_length=16)
    slug = models.CharField("Slug", max_length=32)
    payment_methods = models.ManyToManyField("booking.PaymentMethod")
    is_coupon = models.BooleanField(_("Is coupon"), default=False)
    shipping_cost = models.DecimalField(_("Shipping cost"), max_digits=5, decimal_places=2, default=0)
    room = models.ForeignKey("booking.Room", verbose_name=_("Room"), on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _("ProductFamily")
        verbose_name_plural = _("ProductFamilies")

    def __str__(self):
        return self.name

    def from_price(self):
        return self.products.all().order_by('price').first().price

    def get_absolute_url(self):
        return reverse("ProductFamily_detail", kwargs={"pk": self.pk})


class Room(models.Model):
    """Represents a physical room of the Escape Room.
    TODO: add description, picture, fields
    """
    name = models.CharField(_("Name"), max_length=50)
    is_active = models.BooleanField(_("Active"), default=False)
    description = models.TextField(_("Description"), blank=True, null=True)
    photo = models.ImageField(_("Image"), upload_to='uploads/rooms', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    photo_alt = models.CharField(_("Alt text"), max_length=128, null=True, blank=True)
    theme_colour = models.CharField(_("Colour Hexagesimal"), max_length=6, default="999999")

    def get_page(self):
        if self.room_page:
            return self.room_page.first()
            

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """A model that acts as an iterface for creating Slots, basically is a model that helps in the 
    batch creation/modification of Slots"""
    start_date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("End Date"), auto_now=False, auto_now_add=False)
    dow = models.PositiveSmallIntegerField(_("Day of Week"))
    start_time = models.TimeField(_("Start Time"), auto_now=False, auto_now_add=False)
    interval = models.PositiveSmallIntegerField(_("Interval"), default=30)
    duration = models.PositiveSmallIntegerField(_("Duration"), default=60)
    # room = models.ForeignKey("booking.Room", verbose_name=_("room"), on_delete=models.CASCADE)
    instances = models.PositiveSmallIntegerField(_("Instances"))
    product_family = models.ForeignKey("booking.ProductFamily", verbose_name=_("ProductFamily"), on_delete=models.CASCADE, null=True, blank=True)

    @property
    def room(self):
        return self.product_family.room

    @property
    def end_time(self):
        """
        returns the end time of the schedule
        """
        start_datetime = datetime(100, 1, 1, self.start_time.hour, self.start_time.minute, 0)
        deltaminutes = self.instances * (self.interval + self.duration)
        endtime = start_datetime + timedelta(minutes=deltaminutes)
        return endtime.time()

    class Meta:
        ordering = ["product_family__room", "start_date", "start_time"]     

    def __str__(self):
        return str(self.pk) + self.room.__str__() + str(self.dow_as_integerlist())

    def dow_as_integerlist(self):
        """returns a list of integers corresponding to the day of the week that the schedule
        affects, monday=0 sunday=6, e.g. [2, 4, 6] means Wednesday, Friday, Sunday"""
        dow_binary_list = self.dow_as_binarylist()
        dow_integer_list = list()
        for i, d in enumerate(dow_binary_list):
            if d:
                dow_integer_list.append(i)
        return dow_integer_list

    def save(self, *args, **kwargs):
        """custom save method, checks for collisions with other schedules and creates 
        slots acording to the schedule""" 
        if self.schedule_collision().exists():
            pass

        else:
            super(Schedule, self).save(*args, **kwargs)
            self.delete_slots()
            self.create_new_slots()

    def delete(self, *args, **kwargs):
        """custom delete method, deletes"""
        super(Schedule, self).delete(*args, **kwargs)
        self.delete_slots()

    def get_schedules_same_date(self, schedules=False):
        """Returns Schedule queryset that intersect in dates. Accurate to the day (inclusive)"""
        if not(schedules):
            schedules = Schedule.objects.filter(product_family__room=self.room)
        schedules = schedules.exclude(pk=self.pk)
        return schedules.filter(start_date__lte=self.end_date).exclude(end_date__lt=self.start_date)
    
    def get_schedules_same_time(self, schedules=False):
        """Returns Schedule queryset that intersect in time. Accurate to the minute (non inclusive)"""
        if not(schedules):
            schedules = Schedule.objects.filter(product_family__room=self.room)
        schedules = schedules.exclude(pk=self.pk)
        schedules = schedules.filter(start_time__lt=self.end_time)

        # fills the a list with pks of Schedules to be excluded
        pk_intersects = list()
        for schedule in schedules:
            if schedule.end_time <= self.start_time:
                pk_intersects.append(schedule.pk)
        
        for pk in pk_intersects:
            schedules = schedules.exclude(pk=pk)

        return schedules

    def get_schedules_same_dow(self, schedules=False): 
        if not(schedules):
           schedules = Schedule.objects.filter(room=self.room)
        schedules = schedules.exclude(pk=self.pk)
        schedule_dows = self.dow_as_integerlist()

        # fills the a list with pks of Schedules to be excluded
        pk_intersects = list()
        for schedule in schedules:
            if not(set(schedule.dow_as_integerlist()) & set(schedule_dows)):
                pk_intersects.append(schedule.pk)

        for pk in pk_intersects:
            schedules = schedules.exclude(pk=pk)
        return schedules

    def schedule_collision(self):
        """returns a queryset with the schedules that collide after testing against
        date, time, and day of week"""
        schedules = self.get_schedules_same_date()
        if schedules:
            schedules = self.get_schedules_same_time(schedules)
        if schedules:
            schedules = self.get_schedules_same_dow(schedules)
        return schedules
            

    def create_new_slots(self):
        """returns a list of Slot objects corresponding to the schedule"""
        slots = list()
        curr_date = self.start_date
        if curr_date <= timezone.now().date():
            curr_date = timezone.now().date()
        dow_binary = self.dow_as_binarylist()
        dow_integer = self.dow_as_integerlist()
        while curr_date <= self.end_date:
            if curr_date.weekday() in dow_integer:
                curr_time = self.start_time
                for i in range(0, self.instances):
                    slot = Slot()
                    slot.start = make_aware(datetime.combine(curr_date, curr_time))
                    slot.duration = self.duration
                    slot.interval = self.interval
                    slot.room = self.room
                    slot.schedule = self
                    slot.product_family = self.product_family
                    slot.save()
                    curr_time = addmins(curr_time, self.duration + self.interval)
            curr_date = curr_date + timedelta(days=1)
    
    def dow_as_binarylist(self):
        """returns a list of binary digits from converting the integer that represents the days of the week
        for instance int 1 is 0000001 binary and represents mondays only, 127 is 1111111, which would represent
        every day form sunday to monday"""
        binlist = list('{0:07b}'.format(self.dow))
        binlist.reverse()
        return [int(x) for x in binlist]

    def check_slot_collision(self, slots):
        """checks a list of ordered slots for collisions comparing the calculated end time
        with the start time of the next slot"""
        collision = False
        for i, slot in enumerate(slots):
            if i < len(slots) - 1:
                slot_end = slot.start + timedelta(minutes=slot.duration + slot.interval)
                next_slot = slots[i + 1]
                if slot.is_same_time(next_slot):
                    collision = True
        return collision
    
    def delete_slots(self):
        """deletes slots that are part of this Schedule and that have no related booking"""
        Slot.objects.filter(schedule=self).filter(cart_items__isnull=True, is_disabled=False).delete()

                
class Slot(models.Model):
    """A bookable slot in the calendar, slots are created automatically when saving Schedule objects and are 
    not supposed to be modified directly by the user
    
    Attributes:
        start: Datetime.
        duration: Int in minutes.
        interval: Int in minutes, buffer that prevents new slots being created with a start too close to the previous
        schedule: relation to Schedule Objects
        protect: Bool, if true, the slot is fixed and stops being affected by it's schedule
    """
    start = models.DateTimeField(_("Start"), auto_now=False, auto_now_add=False)
    duration = models.PositiveSmallIntegerField(_("Duration"), default=60)
    interval = models.PositiveSmallIntegerField(_("interval"), default=30)
    room = models.ForeignKey("booking.Room", verbose_name=_("room"), on_delete=models.CASCADE)
    schedule = models.ForeignKey("booking.Schedule", verbose_name=_("schedule"), related_name=("slots"), on_delete=models.SET_NULL, null=True)
    protect = models.BooleanField("protect", null=True)
    product_family = models.ForeignKey("booking.ProductFamily", verbose_name=_("ProductFamily"), on_delete=models.CASCADE, null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['room', 'start']
    
    @property
    def end(self):
        return self.start + timedelta(minutes=self.duration + self.interval)
    
    @property
    def session_end(self):
        return self.start + timedelta(minutes=self.duration)
        
    @property
    def is_available(self):
        return not self.is_reserved() and not self.is_affected_by_buffer() and not self.is_disabled

    @property
    def is_available_to_staff(self):
        return not self.is_reserved()

    def is_booked(self):
        for item in self.cart_items.all():
            if item.status > 0:
                return True
    
    def is_reserved(self):
        for item in self.cart_items.all():
            if item.status > 0 or (item.status == 0 and item.item_expiry() >= timezone.now()):
                return True
        return False 
    
    
    def is_affected_by_buffer(self):
        return not self.is_future_of_buffer() and not self.is_adjacent_after_to_taken_slot()

    def is_future_of_buffer(self):
        this_moment = timezone.now()
        buffer = this_moment + timedelta(minutes=get_booking_settings().slot_buffer_time)
        if self.start > buffer:
            return True
        else:
            return False
        
    def is_adjacent_after_to_taken_slot(self):
        slots = self.get_before_after_minutes_slots(20, 110)
        for slot in slots:
            if slot.is_booked():
                return True
        return False
        
    def is_adjacent_to_taken_slot(self):
        slots = self.get_before_after_minutes_slots(110, 110)
        for slot in slots:
            if slot.is_booked():
                return True
        return False

    def is_parallel_to_taken_slot(self):
        slots = self.get_before_after_minutes_slots(20, 20)
        for slot in slots:
            if slot.is_booked():
                return True
        return False

    def get_before_after_minutes_slots(self, before, after):
        """ Uses the start of sessions as reference
        """
        upper_bound = self.start + timedelta(minutes=before)
        lower_bound = self.start - timedelta(minutes=after)
        return Slot.objects.filter(start__lte=upper_bound, start__gte=lower_bound)

    def incentive_discount(self):
        if self.is_parallel_to_taken_slot():
            discount = get_booking_settings().incentive_discount_parallel_slots
        elif self.is_adjacent_to_taken_slot():
            discount = get_booking_settings().incentive_discount_adjacent_slots
        else:
            discount = 0
        return discount

    def __str__(self):
        return self.start.astimezone().strftime("%Y-%m-%d | %H:%M" )
    
    def save(self, *args, **kwargs):
        # booked_slots = Slot.objects.filter(booking__isnull=False)
        # TODO there's room for opmimisation here, the query calls for slots in the same day
        # this courd be improved into just checking if the query exists for specific slots
        slots = Slot.objects.filter(start__date=self.start.date(), room=self.room)
        slots = slots.exclude(pk=self.pk)

        slot_collides = False
        
        for slot in slots:
            if self.is_same_time(slot):
                slot_collides = True
        if slot_collides:
            print (f'{self} collided')
        else:
            n = datetime.today()
            today_date = datetime(n.year, n.month, n.day, 0, 0, 0, 0)
            today_date = make_aware(today_date)
            # saves if slot is in the future
            if self.start > today_date or self.cart_items.all() or self.protect:
                super(Slot, self).save(*args, **kwargs)
            else:
                pass



    def is_same_time(self, other):
        """compares a Slot with other Slot, if there is supperpossision in the scheduled times then returns true"""
        if self.start <= other.start and self.end <= other.start or self.start >= other.end and self.end >= other.end:
            return False
        else:
            return True

