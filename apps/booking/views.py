import calendar
# import datetime
import traceback
import tempfile
import json

from datetime import datetime, timedelta, date
from calendar import monthrange
from dateutil.parser import parse
from email.mime.image import MIMEImage
# from weasyprint import HTML, CSS

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.loader import render_to_string, get_template
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View
from django.urls import reverse_lazy, reverse, path
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.forms import modelformset_factory

from django.contrib.admin.views.decorators import staff_member_required
from apps.wagtail.home.models import CouponsPage, BooknowPage
from breakout.utils import get_booking_settings, textify


from paypal.standard import conf
from weasyprint import HTML, CSS

from .forms import (
    SlotBookingForm,
    InvoiceForm,
    RemoveFromCartForm,
    CustomPaypal,
    ApplyCouponForm,
    AddProductToCartForm,
    CouponGeneratorForm,
    FilterAppointmentsForm,
    FilterOrdersForm,
    PaymentForm,
)
from .utils import (
    get_cart,
    calendar_from_room,
    getProductsFromProductFamily,
    attach_cart_coupons_to_email,
    get_notification_emails_list,
    send_cart_emails,
)

from .models import (
    Invoice,
    PaymentMethod,
    Product,
    ProductFamily,
    Slot,
)

from .coupon.models import Coupon
from .cart.models import Cart, CartCoupon, CartItem

# overriden by routable page
# def booking_calendars(request):
#     cart = get_cart(request)
#     rooms = Room.objects.filter(is_active=True)
#     context = {
#         'cart': cart,
#         'rooms': rooms,
#     }
#     return render(request, 'booking/view_book.html', context)

# overriden by routable page
def coupons(request):

    cart = get_cart(request)
    try:
        online_coupon_family = ProductFamily.objects.get(slug='coupon-online')
        online_coupon_form = AddProductToCartForm(family=online_coupon_family)
    except Exeption as e:
        print(e)
        online_coupon_form = False
    try:
        voucher_family = ProductFamily.objects.get(name='coupon-voucher')
        voucher_form = AddProductToCartForm(family=voucher_family)
    except Exeption:
        voucher_form = False
    context = {
        'cart': cart,
        'online_coupon_form': online_coupon_form,
        'voucher_form': voucher_form,
    }
    return render(request, 'booking/view_coupon.html', context)

def checkout(request):

    cart = get_cart(request)
    cart.set_subtotal()
    cart.apply_coupons()
    cart.set_total()
    invoice_form = InvoiceForm(cart=cart)
    remove_from_cart_form = RemoveFromCartForm()
    apply_coupon_form = ApplyCouponForm()

    coupons_page = CouponsPage.objects.first()
    booknow_page = BooknowPage.objects.first()
    context = {
        'cart': cart,
        'invoice_form': invoice_form,
        'apply_coupon_form': apply_coupon_form,
        'remove_from_cart_form': remove_from_cart_form,
        'coupons_page': coupons_page,
        'booknow_page': booknow_page,
        'nocart': True,
    }
    return render(request, 'booking/view_checkout.html', context)

def purchase(request):
    if request.method == 'POST':
        cart = get_cart(request)
        form = InvoiceForm(request.POST, cart=cart)

        # TODO this needs to be fixed. Hack that prevents the error in the form
        # is_valid() method where get() returns the original queryset from where the
        # choices can be made as the selected option.
        # This hack replaces the original queryset for a new queryset with only the
        # selected option
        print('before the payment')
        payment = PaymentMethod.objects.filter(pk=request.POST.get('payment'))
        form.fields['payment'].queryset = payment

        print(form.errors)
        if form.is_valid():
            cart.extend_items_expiration()
            invoice = form.save()
            cart.update_valid_items()
            cart.invoice = invoice
            cart.save()
            if cart.process_purchase():
                try:
                    send_cart_emails(cart)
                except Exception as e:
                    traceback.print_exc()
                return HttpResponseRedirect(reverse('booking:order', kwargs={'order': invoice.order_number}))
                return HttpResponse('success')
            else:
                return HttpResponse('errors')
        else:
            return HttpResponse('errors')
    else:
        return HttpResponseRedirect('booking:book')


def order_completed(request, order):
    invoice = Invoice.objects.get(order_number=order)
    cart = invoice.cart
    coupons = cart.get_coupon_items()
    appointments = cart.get_appointment_items()
    payment = invoice.payment
    context = {
        'invoice': invoice,
        'cart': invoice.cart,
        'coupons': coupons,
        'appointments': appointments,
        'payment': payment,
        'nocart': True,
    }

    return render(request, 'booking/view-order.html', context)

def paypal_return(request, cart, email):
    print(request)
    print(cart)
    for cart_item_id in request.session['paypal_items']:
        CartItem.objects.get(pk=cart_item_id).extend_expiration()
    cart = Cart.objects.get(pk=int(cart))
    cart.invoice = Invoice(
        payment=PaymentMethod.objects.get(method='paypal'),
        full_name=email,
        email=email,
        phone=email,
        is_privacy=True,
        is_terms=True,
    )
    cart.invoice.save()
    cart.paypal_preapprove()
    print(cart.invoice.order_number)
    return HttpResponseRedirect(reverse('booking:order', kwargs={'order': cart.invoice.order_number}))

def add_product(request):
    if request.method == 'POST':
        cart = get_cart(request)
        form = AddProductToCartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            print(product)
            cart_item = CartItem(product=product, cart=cart)
            cart_item.save()

            return HttpResponseRedirect(reverse('booking:checkout'))
    else:
        return HttpResponseRedirect(reverse(''))


def add_coupon_by_code(request, coupon_code):
    cart = get_cart(request)
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        cart_coupon = CartCoupon(coupon=coupon, cart=cart)
        cart_coupon.save(request=request)
    except Exception as e:
        pass
    return HttpResponseRedirect(request.build_absolute_uri('/book/'))
        
def add_product_by_id(request, product_id):
    cart = get_cart(request)
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem(product=product, cart=cart)
    cart_item.save()
    return HttpResponseRedirect(reverse('booking:checkout'))

def slot_to_cart(request):
    if request.method == 'POST':
        cart = get_cart(request)
        slot_id = request.POST.get('slot_id')
        form = SlotBookingForm(request.POST, slot_id=slot_id)

        if form.is_valid():
            slot_id = form.cleaned_data['slot_id']
            product = form.cleaned_data['product']
            slot = Slot.objects.get(pk=slot_id)
            if slot.is_available:
                booking = CartItem(slot=slot, product=product, cart=cart)
                booking.save()
                return redirect(reverse('booking:checkout'))
            else:
                return redirect(reverse('booking:book'))
        else:
            return redirect(reverse('booking:book'))
    else:
        return redirect(reverse('booking:book'))

def ajax_calendar(request):
    room = request.GET.get('room', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    room = int(room)
    calendar_data = calendar_from_room(year, month, room=room)
    n = datetime.today()
    today_date = datetime(n.year, n.month, n.day, 0, 0, 0, 0)
    # slots = Slot.objects.filter(start__date__gte=today_date)
    # print (slots)
    context = {
        # 'slots': slots,
        # 'available_counter': 0,
        'calendar': calendar_data,
    }
    return render(request, 'booking/ajax_calendar.html', context)

def ajax_admin_calendar(request):
    room = request.GET.get('room', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    room = int(room)
    calendar_data = calendar_from_room(year, month, room=room)
    n = datetime.today()
    today_date = datetime(n.year, n.month, n.day, 0, 0, 0, 0)
    # slots = Slot.objects.filter(start__date__gte=today_date)
    # print (slots)
    context = {
        # 'slots': slots,
        # 'available_counter': 0,
        'calendar': calendar_data,
    }
    return render(request, 'booking/admin/ajax_admin_calendar.html', context)

def ajax_day_available_slots(request):
    year = int(request.GET.get('year', ''))
    month = int(request.GET.get('month', ''))
    day = int(request.GET.get('day', ''))
    room = int(request.GET.get('room', ''))
    day_slots = date(year, month, day)
    slots = Slot.objects.filter(start__date=day_slots).order_by('start')
    if room:
        slots = slots.filter(room=room)
    slots_list = []
    for slot in slots:
        slots_dict = {}
        slots_dict['slot'] = slot
        slots_dict['pk'] = slot.pk
        slots_dict['is_available'] = slot.is_available
        slots_dict['is_editable'] = slot.is_available_to_staff
        slots_dict['is_disabled'] = slot.is_disabled
        slots_dict['start'] = slot.start
        slots_dict['end'] = slot.session_end
        discount = slot.incentive_discount()
        slots_dict['discount'] = discount
        slots_dict['from_price'] = slot.product_family.from_price() - discount 
        slots_list.append(slots_dict)
    context = {
        'slots': slots_list,
    }
    # return JsonResponse({'data': 'test'})
    if room:
        return render(request, 'booking/ajax_date-availability.html', context)
    else:
        print('admin')
        return render(request, 'booking/admin/ajax_admin_date-availability.html', context)



def ajax_slot_booking(request):
    slot_id = int(request.GET.get('slot', ''))
    slot = Slot.objects.get(pk=slot_id)
    # getProductsFromProductFamily(1)  #testing
    slot_booking_form = SlotBookingForm(slot_id=slot_id)
    context = {
        'slot_booking_form': slot_booking_form,
        'slot': slot,
    }
    return render(request, 'booking/ajax_slot-booking.html', context)


def ajax_slot_disable(request):
    slot_id = int(request.GET.get('slot', ''))
    slot = Slot.objects.get(pk=slot_id)
    slot.is_disabled = True
    slot.save()
    return HttpResponse('slot enabled')

def ajax_slot_enable(request):
    slot_id = int(request.GET.get('slot', ''))
    slot = Slot.objects.get(pk=slot_id)
    slot.is_disabled = False 
    slot.save()
    return HttpResponse('slot enabled')

# pdf

def pdf_coupon_code(request, code=''):
    context = {
        'code': code
    }
    html_string = render_to_string('booking/pdf-coupon_code.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    csspath = settings.STATIC_ROOT + 'css/pdf/coupon_code.css'
    pdf = html.write_pdf(stylesheets=[CSS(csspath)])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="coupon.pdf"'
    return response


#  ajax

@csrf_exempt
def ajax_refresh_invoice(request):
    cart = get_cart(request)
    if request.method == 'POST':
        invoice_form = InvoiceForm(cart=cart)
    context = {
        'cart': cart,
        'invoice_form': invoice_form,
    }
    return render(request, 'booking/ajax-invoice_form.html', context)

@csrf_exempt
def ajax_refresh_item(request):
    cart = get_cart(request)
    print('ajax refresh item')
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('item'):
            item_id = data.get('item')
            cart_id = data.get('cart')
            print('view')
            print(cart.pk)
            print(cart_id)
            print(item_id)
            if cart.pk == int(cart_id):
                print('true')
                cart.remove_item(item_id)
            else:
                print('false')
    context = {
        'cart': cart,
    }
    return render(request, 'booking/ajax_item-list.html', context)
    
@csrf_exempt
def ajax_refresh_coupon(request):
    cart = get_cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        # add coupon
        if data.get('code'):
            code = data.get('code')
            code = code.upper()
            
            try:
                coupon = Coupon.objects.get(code=code)
            except ObjectDoesNotExist:
                coupon = None
                if len(code) > 0:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        _('The coupon with the code "%(code)s" does not exist') % {'code': code}
                    )
            if coupon:
                cart_coupon = CartCoupon(cart=cart, coupon=coupon)
                cart_coupon.save(request)

        # delete coupon
        if data.get('cart_coupon'):
            try:
                cart_coupon_id = data.get('cart_coupon')
                cart_id = data.get('cart')
                cart = Cart.objects.get(pk=cart_id)
                cart_coupon = cart.cart_coupons.get(pk=cart_coupon_id)
                code = cart_coupon.coupon.code
                cart_coupon.delete()
                messages.add_message(
                    request,
                    messages.ERROR, 
                    _('The coupon with code "%(code)s" has been removed from your purchase') % {'code': code}
                )
            except:
                pass

    cart.set_subtotal()
    cart.apply_coupons()
    cart.set_total()
    context = {
        'cart': cart,
    }
    return render(request, 'booking/ajax_coupon-list.html', context)

@csrf_exempt
def ajax_apply_coupon(request):

    cart = get_cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        code = code.upper()

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            coupon = None
            if len(code) > 0:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _('The coupon with the code "%(code)s" does not exist') % {'code': code}
                )
        if coupon:
            cart_coupon = CartCoupon(cart=cart, coupon=coupon)
            cart_coupon.save(request)

    context = {
        'cart': cart,
    }
    cart.apply_coupons()
    return render(request, 'booking/ajax_coupon-list.html', context)

@csrf_exempt
def ajax_remove_coupon(request):
    cart = get_cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_coupon_id = data.get('cart_coupon')
        cart_id = data.get('cart')
        cart = Cart.objects.get(pk=cart_id)
        cart_coupon = cart.cart_coupons.get(pk=cart_coupon_id)
        code = cart_coupon.coupon.code
        cart_coupon.delete()
        messages.add_message(
            request, 
            messages.ERROR, 
            _('The coupon with code "%(code)s" has been removed from your purchase') % {'code': code}
        )

    context = {
        'cart': cart,
    }
    return render(request, 'booking/ajax_coupon-list.html', context)

@csrf_exempt
def ajax_checkout_buttons(request):
    print('ajax stuff')
    if request.method == 'POST':
        print('is_post')
        cart = get_cart(request)
        cart.clear_non_valid_items()
        cart.extend_items_expiration()
        data = json.loads(request.body)
        email = data.get('email')
        payment_id = data.get('payment')
        payment = PaymentMethod.objects.get(pk=payment_id)
        shipping = 0
        if cart.is_require_shipping_address:
            shipping = 2

        cart.apply_coupons
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': cart.total,
            'item_number': cart.pk,
            'item_name': 'Breakout Escape Room',
            'currency_code': 'EUR',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return': request.build_absolute_uri(reverse('booking:paypal_return', kwargs={'cart': cart.pk, 'email': email},)),
            'cancel': request.build_absolute_uri(reverse('booking:checkout')),
            'no_shipping': shipping,
            'items': [item.pk for item in cart.cart_items.all()]
        }
        request.session['paypal_items'] = paypal_dict['items']

    paypal_form = CustomPaypal(initial=paypal_dict)
    context = {
        'payment': payment,
        'paypal_form': paypal_form,
    }
    return render(request, 'booking/ajax_checkout-buttons.html', context)


def test_paypal_ipn(request):
    return render(request, 'booking/test_paypal-ipn.html')


###################
#                 #
#   Admin views   #
#                 #
###################

@staff_member_required
def coupon_generator(request):
    from django import urls

    generatorform = CouponGeneratorForm
    context = {
        'form': generatorform,
    }
    if request.method == 'POST':
        form = CouponGeneratorForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']

            if not number:
                number = 1
        
            coupons = []
            for n in range(0, number):
                form = CouponGeneratorForm(request.POST)
                if form.is_valid():
                    coupons.append(form.save(commit=False))
            
            codelist = Coupon.objects.values_list('code')
            Coupon.code_in_bulk(coupons)
            Coupon.objects.bulk_create(coupons)
            messages.add_message(
                request,
                messages.INFO,
                _('Created %(amount)s coupons') % {'amount': number}
            )

            return HttpResponseRedirect(reverse('booking:coupon_generator'))

    return render(request, 'booking/admin/view-coupon_generator.html', context)

@staff_member_required
def order_summary(request, search=None):
    orders = Cart.objects.filter(status=1).order_by('-invoice__order_date')
    start_date_filter = date.today() - timedelta(28)
    end_date_filter = date.today()
    start_date=None
    end_date=None
    payment=None
    if request.method == 'POST':
        form = FilterOrdersForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            search = form.cleaned_data['search']
            payment = form.cleaned_data['payment']
    else:
        form = FilterOrdersForm

    if start_date or end_date:
        start_date_filter = start_date
        end_date_filter = end_date
    if payment:
        orders = orders.filter(invoice__payment=payment)
    if search:
        orders = orders.filter(
            Q(invoice__full_name__icontains=search)
            | Q(invoice__email__icontains=search)
            | Q(invoice__order_number__icontains=search)
        )
    if start_date_filter and not search:
        orders = orders.filter(invoice__order_date__gte=start_date_filter)
    if end_date_filter and not search:
        end_date_filter = end_date_filter + timedelta(days=1)
        orders = orders.filter(invoice__order_date__lt=end_date_filter)
    order_count = 0
    order_total_price = 0 
    for order in orders:
        order_count += 1
        order_total_price += order.total
    
    order_average = order_total_price / order_count if order_count else 0

    context = {
        'form': form,
        'orders': orders,
        'order_count': order_count,
        'order_total_price': order_total_price,
        'order_average': order_average,
    }
    print('where')
    return render(request, 'booking/admin/view-order_summary.html', context)

@staff_member_required
def appointments(request):
    appointments = CartItem.objects.filter(cart__status__gt=0, status__gt=0, slot__isnull=False)
    start_date_filter = date.today()
    end_date_filter = date.today() + timedelta(days=180)
    if request.method == 'POST':
        form = FilterAppointmentsForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            search = form.cleaned_data['search']
            room = form.cleaned_data['room']

            if start_date or end_date:
                start_date_filter = start_date
                end_date_filter = end_date

            if room:
                appointments = appointments.filter(slot__room=room)
            if search:
                appointments = appointments.filter(
                    Q(cart__invoice__full_name__icontains=search)
                    | Q(cart__invoice__email__icontains=search)
                    | Q(cart__invoice__order_number__icontains=search)
                )

    else:
        form = FilterAppointmentsForm
    if start_date_filter:
        appointments = appointments.filter(slot__start__gte=start_date_filter)
    if end_date_filter:
        end_date_filter = end_date_filter + timedelta(days=1)
        appointments = appointments.filter(slot__start__lt=end_date_filter)
    appointments = appointments.order_by('slot__start')
    context = {
        'form': form,
        'appointments': appointments,
    }
    return render(request, 'booking/admin/view-appointments.html', context)


@staff_member_required
def shipping(request):
    if request.method == "POST":
        if 'shipped' in request.POST:
            item_id = request.POST.get('shipped')
            item = CartItem.objects.get(pk=item_id)
            item.marked_shipped = datetime.now()
            item.save()
        
        if 'not_shipped' in request.POST:
            item_id = request.POST.get('not_shipped')
            item = CartItem.objects.get(pk=item_id)
            item.marked_shipped = None 
            item.save()
 
    shipping_items = CartItem.objects.filter(product__family__shipping_cost__gt=0, status=1)
    to_ship = shipping_items.filter(marked_shipped__isnull=True)
    shipped = shipping_items.filter(marked_shipped__isnull=False)[:10]

    context = {
        'items': to_ship,
        'shipped': shipped,
    }
    return render(request, 'booking/admin/view-shipping.html', context)

@csrf_exempt
@staff_member_required
def change_slot_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        current = Slot.objects.get(pk=data.get('current'))
        order = data.get('order')
        customer = data.get('customer')
        cart_item = data.get('cartitem')
        frompage = data.get('frompage')
        from_date = date.today()
        items = Slot.objects.filter(start__gte=from_date)
        items = items.order_by('start')
        items = [x for x in items if x.is_available_to_staff]
        context = {
            'current': current,
            'cart_item': cart_item,
            'items': items,
            'order': order,
            'customer': customer,
            'frompage': frompage,
        }
        # return JsonResponse({'data': 'test'})
        return render(request, 'booking/admin/ajax-change_slot_list.html', context)

@csrf_exempt
@staff_member_required
def change_product_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        current = Product.objects.get(pk=data.get('current'))
        order = data.get('order')
        customer = data.get('customer')
        cart_item = data.get('cartitem')
        frompage = data.get('frompage')
        from_date = date.today()
        items = Product.objects.filter(family=current.family)
        context = {
            'current': current,
            'cart_item': cart_item,
            'items': items,
            'order': order,
            'customer': customer,
            'frompage': frompage,
        }
        # return JsonResponse({'data': 'test'})
        return render(request, 'booking/admin/ajax-change_product_list.html', context)

@staff_member_required
def change_slot(request):
    if request.method == 'POST':
        valid = False
        frompage = request.POST.get('frompage')
        redirectto = reverse('appointments_list')
        if frompage == 'orders_list':
            redirectto = reverse('orders_list')
            valid = True
        new_slot_id = request.POST.get('new_slot')
        cart_item_id = request.POST.get('cart_item')
        new_slot = Slot.objects.get(pk=new_slot_id) 
        cart_item = CartItem.objects.get(pk=cart_item_id)
        current_product = cart_item.product

        cart_item.slot = new_slot
        # change the product to be aligned with the corresponding room
        # in case it was changed
        if not (new_slot.room == cart_item.product.family.room):
            valid_families = ProductFamily.objects.filter(room=cart_item.slot.room)
            valid_products = Product.objects.filter(family__in=valid_families)
            valid_products = valid_products.order_by('price')
            new_product = valid_products[0]
            # search for a suitable product
            for product in valid_products:
                print(product.price, current_product.price)
                if product.price > current_product.price:
                    break
                else:
                    new_product = product

            cart_item.product = new_product
        cart_item.save()
    return HttpResponseRedirect(redirectto)

@staff_member_required
def delete_order(request):
    if request.method == 'POST':
        frompage = request.POST.get('frompage')
        redirectto = reverse(frompage)
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(pk=cart_id)
        cart.delete_order()

        return HttpResponseRedirect(redirectto)

@staff_member_required
def resend_email(request):
    if request.method == 'POST':
        frompage = request.POST.get('frompage')
        redirectto = reverse(frompage)
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(pk=cart_id)
        cart.send_cart_emails()
        return HttpResponseRedirect(redirectto)


@staff_member_required
def change_product(request):
    if request.method == 'POST':
        frompage = request.POST.get('frompage')
        redirectto = reverse('orders_list')
        new_product_id = request.POST.get('new_slot')
        cart_item_id = request.POST.get('cart_item')
        new_product = Product.objects.get(pk=new_product_id) 
        cart_item = CartItem.objects.get(pk=cart_item_id)
        current_product = cart_item.product

        cart_item.product = new_product 
        cart_item.save()
    return HttpResponseRedirect(redirectto)


@staff_member_required
def record_payment(request):
    if request.method == 'POST':
        sumbited_form = PaymentForm(request.POST)
        if sumbited_form.is_valid:
            sumbited_form.save()
        HttpResponseRedirect(reverse('admin:record_payment'))
    invoices = Invoice.objects.all()
    invoices_list = []
    due_invoices_list = []
    for invoice in invoices:
        if not invoice.is_paid():
            invoices_list.append({
                'invoice': invoice,
                'form': PaymentForm(initial={'invoice': invoice})
            })
            if invoice.is_due :
                due_invoices_list.append({
                    'invoice': invoice,
                    'form': PaymentForm(initial={'invoice': invoice})
                })
    context = {
        'due_list': due_invoices_list,
        'inv_list': invoices_list,
    }
    return render(request, 'booking/admin/view-record_payment.html', context)


@staff_member_required
def slots_calendar(request):
    context = {
        'test': 'test',
    }
    return render(request, 'booking/admin/view-slots_calendar.html', context)

def test_email_template(request, mailto, is_html_or_text=True):
    html_message = render_to_string('email/test_mail.html')
    message = textify(html_message)
    to_email = mailto
    mail_subject = 'Test email'

    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=message,
        from_email='info@breakout-escaperoom.de',
        to=[to_email, ],
    )
    email.attach_alternative(html_message, mimetype='text/html')
    email.content_subtype = 'html'
    email.mixed_subtype = 'related'
    
    img_path = settings.STATIC_ROOT + 'img/icons/yt.png'
    image_name = 'yt.png'
    with open(img_path, 'rb') as f:
        image = MIMEImage(f.read(), _subtype="png")
        email.attach(image)
        image.add_header('Content-ID', "<{}>".format(image_name))

    email.send
    print(email.to)

    if is_html_or_text: 
        return HttpResponse(email)
    return HttpResponse(email)

def test_email_order(request, order):
    invoice = Invoice.objects.get(order_number=order) 
    cart = invoice.cart
    context = {
        'invoice': invoice,
        'cart': cart,
        'domain': 'breakout-escaperoom.de',
        'appointments': cart.get_appointment_items(),
        'coupons': cart.get_coupon_items(),
        'payment': invoice.payment,
    }
    email = render_to_string('email/order_confirmation.html', context)
    # email = textify(email)
    return HttpResponse(email)

