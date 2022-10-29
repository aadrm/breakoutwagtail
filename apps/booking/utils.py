# form python
import re

from calendar import monthrange, Calendar, MONDAY
from datetime import datetime, timedelta, date
from dateutil.parser import parse

from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.mail import send_mail, EmailMultiAlternatives

from breakout.utils import get_booking_settings, booking_limit_date, textify

from weasyprint import HTML, CSS

from .models import Slot, ProductFamily, Room
from .cart.models import Cart

def get_notification_emails_list():
    """returns a list of email addresses from the booking_settings email list"""
    email_str = get_booking_settings().booking_notification_emails
    if email_str:
        email_list = re.split(r', *', email_str)
        return email_list 
    else:
        return ''

def send_cart_emails(cart):
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
    cart.attach_cart_coupons_to_email(email)
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
        to=get_notification_emails_list(),
    )
    email.attach_alternative(html_message, mimetype='text/html')
    email.send(fail_silently=True)


def calendar_from_room(year, month, room):
    """returns a dictionary with slots data of the given calendar month for a room"""
    calendar_data = {}
    if room:
        calendar_data['room'] = Room.objects.get(pk=room)

    calendar_data.update(prepare_calendar_base(year, month, room))

    return calendar_data

def prepare_calendar_base(year, month, room):
    """from a given year and month, it returns the required data to make an html calendar"""

    # this function interfaces with the Slots module
    def callendar_day_to_datadict(day, room):
        """return a dictionary with slot information for the given day"""
        if room:
            slots_in_day = Slot.objects.filter(start__date=day, room=room)
        else:
            slots_in_day = Slot.objects.filter(start__date=day)
        available_slots = 0
        for slot in slots_in_day:
            slot_num += 1
            if slot.is_available:
                available_slots += 1
        day_data = {}
        day_data.update({
            'date': day,
            'slots': slot_num,
            'available_slots': available_slots,
        })
        return day_data

    def get_available_dates(year, month, room):
        if room:
            slots = Slot.objects.filter(start__month=month, start__year=year, room=room) 
            print(booking_limit_date())
            slots = slots.exclude(start__gt=booking_limit_date())
        else:
            slots = Slot.objects.filter(start__month=month, start__year=year) 
            return [s.start.date() for s in slots]
        slots = slots.filter(start__gte=datetime.now())
        available_dates = []
        for slot in slots:
            if slot.is_available:
                available_dates.append(slot.start.date())
        return available_dates

    now = timezone.now().date()
    if year:
        year = int(year)
    else:
        year = now.year
    if month:
        month = int(month)
    else:
        month = now.month
    cal = Calendar(MONDAY)

    month_days = cal.monthdatescalendar(year, month)
    first_day_month = date(year, month, 1)
    last_day_month = date(year, month, monthrange(year, month)[1])
    start_date = first_day_month
    if date.today() > first_day_month:
        start_date = date.today() + timedelta(days=1)
    next_year = year
    next_month = month + 1
    today_year = now.year
    today_month = now.month
    previous_year = year
    previous_month = month - 1
    
    if next_month > 12:
        next_month = 1
        next_year += 1
    if previous_month < 1:
        previous_month = 12
        previous_year -= 1
    
    slots = get_available_dates(year, month, room)

    for i, week in enumerate(month_days):
        for j, day in enumerate(week):
            if month_days[i][j] in slots:
                month_days[i][j] = {'date': month_days[i][j], 'available':True}
            else:
                month_days[i][j] = {'date': month_days[i][j]}

    calendar_base = {
        'month': month,
        'year': year,
        'month_days': month_days,
        'next_month': next_month,
        'next_year': next_year,
        'today_year': today_year,
        'today_month': today_month,
        'previous_year': previous_year,
        'previous_month': previous_month,
        'first_day_month': first_day_month,
    }
    return calendar_base

def getProductsFromProductFamily(product_family_id):
    """returns a list of tuples with with the name and id of the products in a product family
    by using said product family id number"""
    family = ProductFamily.objects.get(pk=product_family_id)
    products = family.products.all()
    products_list = []
    for product in products:
        products_list.append((product, product.pk))
    return products_list

# cart cookies
def check_cart_cookie(request):
    if 'cart_id' not in request.session:
        c = Cart()
        c.save()
        request.session['cart_id'] = c.pk
    else:
        if Cart.objects.filter(pk=request.session['cart_id']).exists():
            c = Cart.objects.get(pk=request.session['cart_id'])
            if not(c.status == 0):
                c = Cart()
                c.save()
                request.session['cart_id'] = c.pk
        else:
            c = Cart()
            c.save()
            request.session['cart_id'] = c.pk
    return request.session['cart_id']

def get_cart(request):
    cart_id = check_cart_cookie(request)
    cart = Cart.objects.get(pk=cart_id)
    return cart

def attach_cart_coupons_to_email(email, cart):
    """given an EmailMessage object and a Cart, this function will create the pdf files of the coupons that
    were purchased in that order and attache them to the email message"""
    for coupon in cart.get_coupon_items():
        context = {
            'coupon': coupon.coupon,
        }
        html_string = render_to_string('booking/pdf-coupon_code.html', context)
        html = HTML(string=html_string, base_url=settings.BASE_URL)
        # html = HTML(string=html_string, base_url=request.build_absolute_uri())
        csspath = settings.STATIC_ROOT + 'css/pdf/coupon_code.css'
        pdf = html.write_pdf(stylesheets=[CSS(csspath)])
        email.attach(_('gift_voucher_') + coupon.coupon.code + '.pdf', pdf)

