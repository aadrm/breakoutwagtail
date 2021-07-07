import traceback
from datetime import datetime, timedelta, time, date

from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django.utils import timezone
from django.utils.timezone import make_aware, is_aware
from django.db import models, transaction
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from breakout.utils import get_booking_settings, textify


from weasyprint import HTML, CSS
# from phonenumber_field.modelfields import PhoneNumberField

from breakout.utils import addmins


# Create your models here

class Cart(models.Model):
    """
    Shopping Cart

    A cart is created for every session. 
    Producs and coupons are added to a cart by using the models CartItem and CartCoupon.
    """

    status = models.SmallIntegerField(_("status"), default=0)
    items_before_checkout = models.SmallIntegerField(_("items before purchase"), blank=True, null=True)
    invoice = models.OneToOneField("booking.Invoice", verbose_name=_("Invoice"), on_delete=models.PROTECT, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    @property
    def is_require_shipping_address(self):
        for item in self.get_valid_items():
            if item.product.family.shipping_cost:
                return True
        return False

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def get_absolute_url(self):
        return reverse("Cart_detail", kwargs={"pk": self.pk})

    def apply_coupons(self):
        cart_items = self.get_valid_items()
        self.reset_cart_items()

        for coupon in self.cart_coupons.all():
            cp = coupon.coupon
            applicable_products = cp.products_applicable_queryset()
            applied = False
            #  used for cases where a fixed amount discount that applies to the entire basquet
            #  has more value than the current item of the basquet, so the rest of the coupon
            #  will be applied to the next item
            cumulative_discount = 0
            for item in cart_items:
                applicable_to_product = cp.is_applicable(item.product, applicable_products)
                applicable_to_slot = True
                if item.slot:
                    applicable_to_slot = False
                    if item.slot.start.weekday() in cp.dow_as_integerlist:
                        applicable_to_slot = True
                if applicable_to_product and applicable_to_slot:
                    if coupon.no_coupon_conflict(item):
                        cumulative_discount = coupon.add_to_cart_item(item, cumulative_discount)
                        applied = True
                        if not(cp.is_apply_to_basket) or not(cp.is_percent) and cumulative_discount >= cp.amount:
                            break
            self.print_items_prices()

    @transaction.atomic
    def reset_cart_items(self):
        self.reset_cart_items_price()
        self.reset_cart_items_coupons()
        self.reset_cart_coupons()

    def reset_cart_items_price(self):
        for item in self.get_valid_items():
            item.price = item.base_price
            item.save()

    def reset_cart_items_coupons(self):
        for item in self.get_valid_items():
            item.cart_coupons.clear()
            item.save()
    
    def reset_cart_coupons(self):
        for coupon in self.cart_coupons.all():
            coupon.discount = 0
            coupon.save()


    def get_valid_items(self):
        items = self.cart_items.all()
        for item in items:
            if not item.is_in_cart:
                item.delete()
        return items 

    # def get_valid_items_queryset(self):
    #     pks = [item.pk for item in self.get_valid_items()]
    #     return CartItem.objects.filter(pk__in=pks)

    def get_appointment_items(self):
        valid_items = self.get_valid_items()
        appointment_items = []
        for item in valid_items:
            if item.slot:
                appointment_items.append(item)
        return appointment_items

    def get_coupon_items(self):
        valid_items = self.get_valid_items()
        coupon_items = []
        for item in valid_items:
            if item.product.family.is_coupon:
                coupon_items.append(item)
        return coupon_items

    def print_items_prices(self):
        print('---items---')
        for item in self.get_valid_items():
            print(f'{item}: price {item.price} base {item.base_price}')

    def get_valid_payment_methods(self):
        methods_prev = PaymentMethod.objects.filter(method='coupon')
        if self.total_after_coupons() > 0:
            items = self.get_valid_items()
            methods_prev = PaymentMethod.objects.all()
            methods_curr = PaymentMethod.objects.all()
            for item in items:
                methods_curr = item.product.family.payment_methods.all()
                methods_prev = methods_curr.intersection(methods_prev)
        return methods_prev

    def number_of_valid_items(self):
        """return the number of valid items, useful in the templates"""
        itemsList = list(self.get_valid_items())
        return len(itemsList)

    def update_valid_items(self):
        """this method checks the valid items currently on the cart
        meant to save this 'status' during checkout and later compare this number
        when trying to execute payment and accept the transaction if both numbers match
        """
        self.items_before_checkout = self.number_of_valid_items()
        self.save()

    def total(self):
        """The sum of the price of the valid items in the cart"""
        total = 0
        items = self.get_valid_items()
        for item in items:
            total += item.base_price
        return total
    
    def total_after_coupons(self):
        """The sum of the price of the valid items in the cart
        after the discount of the coupons in the cart is applied"""
        total = 0
        items = self.get_valid_items()
        for item in items:
            total += item.price
        return total

    def discount(self):
        """
        Subtraction between total and total_after_coupons
        """
        return self.total() - self.total_after_coupons()

    def extend_items_expiration(self):
        """calls the extend expiration method for each of the cart items"""
        for item in self.get_valid_items():
            item.extend_expiration()

    def use_coupons(self):
        """
        Calls the function that increases the use counter for each coupon in the cart
        """
        for coupon in self.cart_coupons.all():
            coupon.coupon.add_used_time()
    
    def approve_items(self):
        """
        sets the status of all the items of the cart to 1 which means that
        each item has ben purchased
        """
        for item in self.get_valid_items():
            print('a valid item')
            item.set_approved()
            item.save()

    def create_cart_coupons(self, paid=True):
        coupon_items = self.get_coupon_items()
        for item in coupon_items:
            if item.coupon:
                coupon = item.coupon
            else:
                coupon = Coupon()

            value = item.base_price - item.product.family.shipping_cost
            coupon_ref = ''
            coupon_ref += self.invoice.order_number
            coupon_ref = ' | '
            coupon_ref += item.product.__str__()
            coupon.use_limit = 1 if paid else -1
            coupon.name = coupon_ref
            coupon.is_apply_to_basket = True
            coupon.amount = value
            coupon.is_overrule_individual_use = False
            coupon.is_individual_use = False
            coupon.save()

            item.coupon = coupon
            item.save()

    def paypal_preapprove(self):
        if self.status < 1:
            self.status = 2
            self.invoice.commit_order()
            self.create_cart_coupons(paid=False)
            self.save()

    def approve_cart(self):
        """
        sets the status of the cart to 1 which means that the order should be confirmed
        """
        print('approving cart')
        self.approve_items()
        self.use_coupons()
        self.status = 1
        self.save()

    def process_purchase(self):
        try:
            print('---------------approve cart')
            self.approve_cart()
            print('invoice')
            self.invoice.commit_order()
            self.create_cart_coupons()
            return True
        except Exception as e:
            print(e)
            return False

    def send_cart_emails(self):
        cart = self
        invoice = cart.invoice
        context = {
            'invoice': invoice,
            'cart': cart,
            'domain': 'breakout-escaperoom.de',
            'appointments': cart.get_appointment_items(),
            'coupons': cart.get_coupon_items(),
            'payment': invoice.payment.method,
        }

        html_message = render_to_string(
            'email/order_confirmation.html', context)
        message = textify(html_message)
        to_email = invoice.email
        mail_subject = _('Breakout Escape Room | Order: ') + \
            invoice.order_number
        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,
            from_email='info@breakout-escaperoom.de',
            to=[to_email, ],
        )

        email.attach_alternative(html_message, mimetype='text/html')
        self.attach_cart_coupons_to_email(email)
        email.send(fail_silently=True)

        mail_subject = _('Breakout Escape Room | Order: ') + \
            invoice.order_number
        html_message = render_to_string(
            'email/order_confirmation_alert.html', context)
        message = textify(html_message)

        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,
            from_email='info@breakout-escaperoom.de',
            to=['info@breakout-escaperoom.de', ],
        )
        email.attach_alternative(html_message, mimetype='text/html')
        email.send(fail_silently=True)

    def attach_cart_coupons_to_email(self, email):
        """given an EmailMessage this function will create the pdf files of the coupons that
        were purchased in that order and attache them to the email message"""
        for coupon in self.get_coupon_items():
            context = {
                'coupon': coupon.coupon,
            }
            html_string = render_to_string(
                'booking/pdf-coupon_code.html', context)
            html = HTML(string=html_string, base_url=settings.BASE_URL)
            # html = HTML(string=html_string, base_url=request.build_absolute_uri())
            csspath = settings.STATIC_ROOT + 'css/pdf/coupon_code.css'
            pdf = html.write_pdf(stylesheets=[CSS(csspath)])
            email.attach(_('gift_voucher_') + coupon.coupon.code + '.pdf', pdf)

    def remove_item(self, id):
        print('remove item called')
        items = self.cart_items.all()
        item = items.get(pk=id)
        item.delete()

    def delete_order(self):
        """
        deletes the order and any related data
        """
        for item in self.cart_items.all():
            item.delete()
        for item in self.cart_coupons.all():
            item.coupon.used_times -= 1
            item.coupon.save()
            item.delete()
        invoice = self.invoice
        self.delete()
        invoice.delete()

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class CartItem(models.Model):
    """
    Model that acts as a bridge between products and the cart
    """
    slot = models.ForeignKey("booking.Slot", related_name="booking", verbose_name=_(
        "slot"), on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey("booking.Coupon", related_name="booking",
                               on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey("booking.Product", on_delete=models.PROTECT)
    status = models.SmallIntegerField(_("status"), default=0)
    cart = models.ForeignKey("booking.Cart", verbose_name=_("Cart"), related_name=_(
        "cart_items"), on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    price = models.DecimalField(
        _("Price"), max_digits=8, decimal_places=2, default=0)
    cart_coupons = models.ManyToManyField("booking.CartCoupon", verbose_name=_(
        "coupons"), related_name='cart_items', blank=True)
    marked_shipped = models.DateTimeField(
        _("Shipped"), auto_now=False, auto_now_add=False, null=True, blank=True)

    @property
    def is_appointment(self):
        True if self.slot else False

    @property
    def is_coupon(self):
        True if self.product.family.is_coupon else False

    @property
    def base_price(self):
        return self.product.price

    @property
    def is_slot_booked(self):
        """
        Returns True if there is a slot associated with this item and either 
        the booking was completed or is being booked and the expiry time has not been reached
        """
        if self.slot:
            this_moment = timezone.now()
            print('now', this_moment)
            print('expiry', self.slot_expiry)

            if self.status > 0:
                print ('status > 0')
                return True
            elif self.status == 0 and this_moment < self.slot_expiry:
                print ('time?', this_moment < self.slot_expiry)
                return True
            else:
                return False
        else:
            return False

    @property
    def slot_expiry(self):
        """
        returns the datetime of expiration for this item, only affects the item if it has 
        a related slot and status is 0 
        """
        if self.slot:
            return self.created + timedelta(minutes=get_booking_settings().slot_reservation_hold_minutes)
        else:
            False

    @property
    def is_in_cart(self):
        """this means that the item is part of it's related cart, the conditions are if 
        this item is not expired
        """
        print(self.slot_expiry_seconds())
        if self.slot and self.status == 0  and self.slot_expiry_seconds() < 1:
            return False
        elif self.status < 0:
            return False
        else:
            print('in_cart')
            return True

    def slot_expiry_seconds(self):
        if self.slot and self.status == 0:
            this_moment = timezone.now()
            expiry = self.slot_expiry 
            # this condition allows some extra time for orders carried out via paypal IPN
            if self.cart.status > 0:
                return ((expiry + timedelta(minutes=40)) - this_moment).total_seconds()
            else:
                return (expiry - this_moment).total_seconds()
        else:
            return 0

    def save(self, request=None, *args, **kwargs):
        """
        Custom save method, sets the price of the CartItem to be the same as the product's
        This price is the one to be modified by any discounts applied.
        """

        if self.pk is None:
            self.price == self.product.price

        super(CartItem, self).save(*args, **kwargs)

    def extend_expiration(self):
        self.created = timezone.now() 
        self.save()

    def set_approved(self):
        self.status = 1
        self.save()

    def has_individual_use_coupon(self):
        if self.cart_coupons.filter(coupon__is_individual_use=True):
            return True
        else:
            return False

    def has_neutral_coupon(self):
        if self.cart_coupons.filter(coupon__is_overrule_individual_use=False):
            return True
        else:
            return False

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

class CartCoupon(models.Model):

    coupon = models.ForeignKey("booking.Coupon", verbose_name=_("Cart Coupon"), null=True, on_delete=models.SET_NULL, )
    cart = models.ForeignKey("booking.Cart", verbose_name=_("Cart"), related_name=_("cart_coupons"), on_delete=models.CASCADE, null=True, blank=True)
    discount = models.DecimalField(_("Discount"), max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("CartCoupon")
        verbose_name_plural = _("CartCoupons")
        ordering = [
            '-coupon__is_upgrade',
            'coupon__is_percent',
            'coupon__is_apply_to_basket',
        ]

    def __str__(self):
        return self.coupon.__str__()

    def get_absolute_url(self):
        return reverse("CartCoupon_detail", kwargs={"pk": self.pk})

    def save(self, request=None, *args, **kwargs):

        """Custom save method checks if the coupon is not already in the cart"""
        print(self.coupon.pk)
        if request:
            if self.cart.cart_coupons.filter(coupon__pk=self.coupon.pk).exists():
                messages.add_message(
                    request,
                    messages.WARNING,
                    _('The coupon with the code "%(code)s" is already being applied to your purchase.') % 
                    {'code': self.coupon.code}
                )
            elif self.coupon and self.coupon.is_expired:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _('The coupon "%(code)s" is expired') %
                    {'code': self.coupon.code}

                )
            elif self.coupon and self.coupon.is_overused:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _('The "%(code)s" has exceeded its usage limit') %
                    {'code': self.coupon.code}
                )
            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    _('Coupon "%(code)s" successfully added to your cart') %
                    {'code': self.coupon.code}
                )
                super(CartCoupon, self).save(*args, **kwargs)
        else:
            super(CartCoupon, self).save(*args, **kwargs)

    def no_coupon_conflict(self, cart_item):
        if self.coupon.is_overrule_individual_use:
            return True
        elif self.coupon.is_individual_use:
            if not(cart_item.has_neutral_coupon()):
                return True 
            else:
                return False
        else:
            if not(cart_item.has_individual_use_coupon()):
                return True 
            else:
                return False 

    def add_to_cart_item(self, item, cumulative_discount):
        cumulative_discount = self.coupon.apply_to_cart_item(item, cumulative_discount, self)
        self.discount = cumulative_discount
        self.save()
        return cumulative_discount


class Coupon(models.Model):

    def now_plus_time():
        return datetime.today() + timedelta(days=1095)

    def code_in_bulk(objs):
        allowed_chars = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')
        # allowed_chars = ('AB')
        unique = False
        while not unique:
            codes = []
            for obj in objs:
                obj.code = get_random_string(12, allowed_chars)
                codes.append(obj.code)

            if len(set(codes)) == len(codes):
                coupons_same_slug = Coupon.objects.filter(code__in=codes)
                if len(coupons_same_slug) == 0:
                    unique = True

    name = models.CharField(_("reference"), max_length=255, blank=True, null=True)
    code = models.SlugField(_("code"), max_length=32, blank=True, unique=True)
    amount = models.DecimalField(_("discount amount"), max_digits=5, decimal_places=2, default=0)
    is_percent = models.BooleanField(_("is percent"), default=False)
    is_apply_to_basket = models.BooleanField(_("entire basket"), default=False)
    is_individual_use = models.BooleanField(_("can be combined"), default=True)
    is_overrule_individual_use = models.BooleanField(_("can be combined"), default=False)
    is_upgrade = models.BooleanField(_("Upgrades the item"), default=False)
    product_families_included = models.ManyToManyField("booking.ProductFamily", related_name="product_family_include", verbose_name=_(" include families"), blank=True)
    product_families_excluded = models.ManyToManyField("booking.ProductFamily", related_name="product_family_exclude", verbose_name=_(" exclude families"), blank=True)
    product_included = models.ManyToManyField("booking.Product", related_name="product_include", verbose_name=_("include product"), blank=True)
    product_excluded = models.ManyToManyField("booking.Product", related_name="product_exclude", verbose_name=_("exclude product"), blank=True)
    used_times = models.IntegerField(_("Used times"), default=0)
    use_limit = models.IntegerField(_("Usage limit"), default=1)
    created = models.DateTimeField(_("Created"), auto_now=True, auto_now_add=False)
    expiry = models.DateField(_('Expiration date'), blank=True, null=True, default=now_plus_time)
    minimum_spend = models.DecimalField(_("Minimum spend"), max_digits=5, decimal_places=2, default=0)
    dow_valid = models.PositiveSmallIntegerField(_("Days Valid"), default=127) 

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.pk)

    @property
    def is_expired(self):
        is_expired = False
        if self.expiry:
            if self.expiry < datetime.now().date():
                is_expired = True
        return is_expired

    @property
    def is_overused(self):
        if self.use_limit:
            if self.used_times >= self.use_limit:
                return True
            else:
                return False
        else:
            return True

    @property
    def is_valid(self):
        if self.is_overused or self.is_expired:
            return False
        else:
            return True

    @property
    def dow_as_binarylist(self):
        """returns a list of binary digits in reverse from converting the integer that represents the days of the week
        for instance int 1 is 0000001 binary and represents mondays only, 127 is 1111111, which would represent
        every day form sunday to monday"""
        binlist = list('{0:07b}'.format(self.dow_valid))
        binlist.reverse()
        return [int(x) for x in binlist]

    @property
    def dow_as_integerlist(self):
        """returns a list of integers corresponding to the day of the week that the schedule
        affects, monday=0 sunday=6, e.g. [2, 4, 6] means Wednesday, Friday, Sunday"""
        dow_binary_list = self.dow_as_binarylist
        dow_integer_list = list()
        for i, d in enumerate(dow_binary_list):
            if d:
                dow_integer_list.append(i)
        return dow_integer_list

    def add_used_time(self):
        """Increases the counter that tracks how many times a coupon has been applied"""
        print('called used time')
        print(self.used_times)
        self.used_times += 1
        print(self.used_times)
        self.save()

    def get_absolute_url(self):
        return reverse("Coupon_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method. """
        self.code_save()
        super(Coupon, self).save(*args, **kwargs)

    def code_save(obj):
        allowed_chars = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')
        in_set = type(obj).objects.all()
        
        if not obj.code:
            obj.code = get_random_string(12, allowed_chars)
            code_is_wrong = True
            while code_is_wrong:  # keep checking until we have a valid slug
                code_is_wrong = False
                other_coupons_with_same_slug = in_set.filter(code=obj.code)
                if len(other_coupons_with_same_slug) > 0:
                    code_is_wrong = True
                if code_is_wrong:
                    obj.code = get_random_string(12, allowed_chars)
        else:
            obj.code = obj.code.upper()

    def products_included_queryset(self):
        """returns a queryset with the all the producs related in the fields products_included and
        the product_families_included"""
        products = self.product_included.all()
        families = self.product_families_included.all()

        for family in families:
            family_products = family.products.all()
            products = (products | family_products)

        return products.distinct()

    def products_excluded_queryset(self):
        """returns a queryset with the all the producs related in the fields products_excluded and
        the product_families_excluded"""
        products = self.product_excluded.all()
        families = self.product_families_excluded.all()

        for family in families:
            family_products = family.products.all()
            products = (products | family_products).distinct()

        return products.distinct()

    def products_cant_degrade_queryset(self):
        """
        a list of products where coupons that upgrade a product cannot be applied 
        """
        return Product.objects.filter(degrade=None)

    def products_applicable_queryset(self):
        """returns a queryset to with the products to which the coupon is applicable to"""
        if self.products_included_queryset():
            products = self.products_included_queryset()
        else:
            products = Product.objects.all()

        excluded_products = self.products_excluded_queryset()
        if self.is_upgrade:
            # excluded_products = excluded_products.union(self.products_cant_degrade_queryset())
            excluded_products = (excluded_products | self.products_cant_degrade_queryset()).distinct()
        products = products.exclude(pk__in=excluded_products)
        return products

    def is_applicable(self, product, products):
        """checks wether the may be applied to certain product"""
        applicable = False
        applicable = self.is_applicable_by_product(product, products)
        return applicable

    def is_applicable_by_product(self, product, products):
        """Checks if the product applicable by taking into consideration the included and excluded
        products and product families"""
        applicable = False
        if product in products:
            applicable = True
        return applicable

    def apply_to_cart_item(self, item, cumulative_discount, cart_coupon):
        price = item.price
        price_before = price
        used = False
        if self.is_percent:
            price = (1 - self.amount / 100) * price
            used = True
        elif self.is_upgrade:
            price = item.product.degrade.price
            used = True
        else:
            price = price - (self.amount - cumulative_discount)
            used = True
            if price < 0:
                price = 0
        if used:
            item.cart_coupons.add(cart_coupon)
            cart_coupon.discout = cumulative_discount
            item.price = price
            item.save()
            cumulative_discount += (price_before - price)
        return cumulative_discount


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
            return self.cart.total_after_coupons()
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
                    print('date', item.slot.start.date(), date.today(),item.slot.start.date() < date.today() )
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
        if self.order_int:
            slug += str(self.order_int).zfill(3)
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
    upgrade = models.OneToOneField("booking.Product", verbose_name=_("upgrade"), related_name='degrade', on_delete=models.SET_NULL, null=True, blank=True)
    family = models.ForeignKey("booking.ProductFamily", verbose_name=_("Family"), related_name='products', on_delete=models.CASCADE, null=True, blank=False)
    players = models.SmallIntegerField(_("Players"), blank=True, null=True)

    class Meta:
        ordering = ['price']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        name_str = ''
        if self.players:
            name_str += str(self.players)
            name_str += ' ' 
            name_str += _('Player')
        name_str += ' | ' + self.family.__str__() 

        return name_str

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

    def has_degrade(self):
        has = False
        try:
            has = (self.degrade is not None)
        except Product.DoesNotExist:
            pass
        return has


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
        
        print (pk_intersects)
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
                print (f'{slot}={next_slot}', end='')
                if slot.is_same_time(next_slot):
                    collision = True
                    print ("collision", end='')
                print ()
        return collision
    
    def delete_slots(self):
        """deletes slots that are part of this Schedule and that have no related booking"""
        Slot.objects.filter(schedule=self).filter(booking__isnull=True, is_disabled=False).delete()

                
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
    protect = models.BooleanField(_("protect"), null=True)
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
        if self.is_not_reserved and self.is_future_of_buffer and not self.is_disabled:
            return True
        else:
            return False 
    
    @property
    def is_not_reserved(self):
        is_free = True
        if self.booking.all().exists():
            bookings = self.booking.all()            
            for booking in bookings:
                if is_free:
                    is_free = not(booking.is_slot_booked)
        return is_free
    
    @property
    def is_future_of_buffer(self):
        this_moment = make_aware(datetime.today()) 
        buffer = this_moment + timedelta(hours=get_booking_settings().slot_buffer_time)
        if self.start > buffer:
            return True
        else:
            return False
    
    def __str__(self):
        return self.room.__str__() + ' | ' + self.start.astimezone().strftime("%Y-%m-%d | %H:%M" ) + '(' + str(self.duration) + ')'
    
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
            if self.start > today_date or self.booking.all() or self.protect:
                super(Slot, self).save(*args, **kwargs)
            else:
                pass

    def is_same_time(self, other):
        """compares a Slot with other Slot, if there is supperpossision in the scheduled times then returns true"""
        if self.start <= other.start and self.end <= other.start or self.start >= other.end and self.end >= other.end:
            return False
        else:
            return True

