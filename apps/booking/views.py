import calendar
# import datetime
import traceback
import tempfile
import json

from datetime import datetime, timedelta, date
from calendar import monthrange
from dateutil.parser import parse
# from weasyprint import HTML, CSS

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.loader import render_to_string, get_template
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.forms import modelformset_factory

from django.contrib.admin.views.decorators import staff_member_required

from breakout.utils import get_booking_settings


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
)

from .models import (
    Room,
    Cart,
    Invoice,
    CartCoupon,
    CartItem,
    Coupon,
    PaymentMethod,
    Product,
    ProductFamily,
    Slot,
)


def booking_calendars(request):
    cart = get_cart(request)
    rooms = Room.objects.filter(is_active=True)
    context = {
        'cart': cart,
        'rooms': rooms,
    }
    return render(request, 'booking/view_book.html', context)

def coupons(request):

    cart = get_cart(request)
    try:
        online_coupon_family = ProductFamily.objects.get(name='CouponOnline')
        voucher_family = ProductFamily.objects.get(name='CouponVoucher')
        online_coupon_form = AddProductToCartForm(family=online_coupon_family)
        voucher_form = AddProductToCartForm(family=voucher_family)
    except Exeption:
        pass
    context = {
        'cart': cart,
        'online_coupon_form': online_coupon_form,
        'voucher_form': voucher_form,
    }
    return render(request, 'booking/view_coupon.html', context)

def checkout(request):

    cart = get_cart(request)
    cart.apply_coupons()
    invoice_form = InvoiceForm(cart=cart)
    remove_from_cart_form = RemoveFromCartForm()
    apply_coupon_form = ApplyCouponForm()
    context = {
        'cart': cart,
        'invoice_form': invoice_form,
        'apply_coupon_form': apply_coupon_form,
        'remove_from_cart_form': remove_from_cart_form,
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
        payment = PaymentMethod.objects.filter(pk=request.POST.get('payment'))
        form.fields['payment'].queryset = payment

        print(form.errors)
        if form.is_valid():
            invoice = form.save()
            cart.update_valid_items()
            cart.invoice = invoice
            cart.extend_items_expiration()
            cart.save()
            if cart.process_purchase():
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
    payment = invoice.payment.method
    context = {
        'invoice': invoice,
        'cart': invoice.cart,
        'coupons': coupons,
        'appointments': appointments,
        'payment': payment,
    }
    return render(request, 'booking/view-order.html', context)

def paypal_return(request, cart, email):
    print(request)
    print(cart)
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
    cart.extend_items_expiration()
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
    calendar_data = calendar_from_room(year, month, room)
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

def ajax_day_available_slots(request):
    year = int(request.GET.get('year', ''))
    month = int(request.GET.get('month', ''))
    day = int(request.GET.get('day', ''))
    room = int(request.GET.get('room', ''))
    day_slots = date(year, month, day)
    slots = Slot.objects.filter(start__date=day_slots)
    slots = slots.filter(room=room)
    context = {
        'slots': slots,
    }
    # return JsonResponse({'data': 'test'})
    return render(request, 'booking/ajax_date-availability.html', context)

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

# pdf

def pdf_coupon_code(request):
    code = 'snthaoeusnnth'
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

        # delete coupon
        if data.get('cart_coupon'):
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
    cart.apply_coupons()
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
    if request.method == 'POST':
        cart = get_cart(request)
        cart.extend_items_expiration()
        data = json.loads(request.body)
        email = data.get('email')
        payment_id = data.get('payment')
        payment = PaymentMethod.objects.get(pk=payment_id)
        shipping = 0
        if cart.is_require_shipping_address:
            shipping = 2

        cart.apply_coupons()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': cart.total_after_coupons,
            'item_number': cart.pk,
            'item_name': 'Breakout Escape Room',
            'currency_code': 'EUR',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return': request.build_absolute_uri(reverse('booking:paypal_return', kwargs={'cart': cart.pk, 'email': email},)),
            'cancel': request.build_absolute_uri(reverse('booking:checkout')),
            'no_shipping': shipping
        }
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

def order_summary(request):
    orders = Cart.objects.filter(status=1)
    start_date_filter = date.today() - timedelta(28)
    end_date_filter = date.today()
    if request.method == 'POST':
        form = FilterOrdersForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            search = form.cleaned_data['search']
            payment = form.cleaned_data['payment']

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

    else:
        form = FilterOrdersForm

    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'booking/admin/view-order_summary.html', context)

@staff_member_required
def appointments(request):
    appointments = CartItem.objects.filter(cart__status__gt=0, status__gt=0, slot__isnull=False)
    start_date_filter = date.today()
    end_date_filter = date.today() + timedelta(days=7)
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
        current_slot = Slot.objects.get(pk=data.get('currentslot'))
        order = data.get('order')
        customer = data.get('customer')
        cart_item = data.get('cartitem')
        frompage = data.get('frompage')
        from_date = date.today()
        slots = Slot.objects.filter(start__gte=from_date)
        slots = slots.order_by('start')
        context = {
            'current_slot': current_slot,
            'cart_item': cart_item,
            'slots': slots,
            'order': order,
            'customer': customer,
            'frompage': frompage,
        }
        # return JsonResponse({'data': 'test'})
        return render(request, 'booking/admin/ajax-change_slot_list.html', context)


def change_slot(request):
    if request.method == 'POST':
        valid = False
        frompage = request.POST.get('frompage')
        if frompage == 'order_summary':
            redirectto = reverse('admin:order_summary')
            valid = True
        elif frompage == 'appointments':
            redirectto = reverse('admin:appointments')
            valid = True
        if valid:
            new_slot_id = request.POST.get('new_slot')
            cart_item_id = request.POST.get('cart_item')
            new_slot = Slot.objects.get(pk=new_slot_id) 
            cart_item = CartItem.objects.get(pk=cart_item_id)
            current_product = cart_item.product

            if new_slot.is_available:
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


def record_payment(request):
    if request.method == 'POST':
        sumbited_form = PaymentForm(request.POST)
        if sumbited_form.is_valid:
            sumbited_form.save()
        HttpResponseRedirect(reverse('admin:record_payment'))
    invoices = Invoice.objects.filter(payments__isnull=True)
    invoices_list = []
    due_invoices_list = []
    for invoice in invoices:
        invoices_list.append({
            'invoice': invoice,
            'form': PaymentForm(initial={'invoice': invoice})
        })
        if invoice.is_due:
            due_invoices_list.append({
                'invoice': invoice,
                'form': PaymentForm(initial={'invoice': invoice})
            })
    context = {
        'due_list': due_invoices_list,
        'inv_list': invoices_list,
    }
    return render(request, 'booking/admin/view-record_payment.html', context)

