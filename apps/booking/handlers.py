from paypal.standard.models import ST_PP_COMPLETED, ST_PP_PENDING
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import Cart, PaymentMethod, Invoice
from .forms import InvoiceForm
from django.conf import settings
from django.dispatch import receiver

@receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    print('ipn signal received')
    ipn_obj = sender
    print(ipn_obj)
    if ipn_obj.payment_status == ST_PP_COMPLETED or ipn_obj.payment_status == ST_PP_PENDING:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        cart = Cart.objects.get(pk=ipn_obj.item_number)
        price = cart.total_after_coupons()

        print(ipn_obj.mc_gross, price)
        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'EUR':
            payment = PaymentMethod.objects.get(method='paypal')
            print(payment)
            invoice = cart.invoice
            if invoice:
                # if the Invoice's attributes ar updated this way the ipn atttributes come as 
                # a tuple, still have to figure out why
                print('first_name', ipn_obj.first_name, type(ipn_obj.first_name))
                print('last_name', ipn_obj.last_name, type(ipn_obj.last_name))
                invoice.full_name=ipn_obj.first_name + ' ' + ipn_obj.last_name,
                print('contact_phone', ipn_obj.contact_phone, type(ipn_obj.contact_phone))
                invoice.phone=ipn_obj.contact_phone,
                print('address_street', ipn_obj.address_street, type(ipn_obj.address_street))
                invoice.street=ipn_obj.address_street,
                print('address_zip', ipn_obj.address_zip, type(ipn_obj.address_zip))
                invoice.post=ipn_obj.address_zip,
                print('adress_city', ipn_obj.adress_city, type(ipn_obj.adress_city))
                invoice.city=ipn_obj.address_city,
                invoice.is_terms=True,
                invoice.is_privacy=True,
                print('invoice updated ipn object ')
                print(invoice.__dict__)
            else:
                print('invoice created on ipn received')
                print(invoice.__dict__)
                invoice = Invoice(
                    full_name=ipn_obj.first_name + ' ' + ipn_obj.last_name,
                    phone=ipn_obj.contact_phone,
                    email=ipn_obj.payer_email,
                    street=ipn_obj.address_street,
                    post=ipn_obj.address_zip,
                    city=ipn_obj.address_city,
                    is_terms=True,
                    is_privacy=True,
                    payment=payment,
                )

            print('invoice before save')
            print(invoice.__dict__)
            invoice.save()
            cart.invoice = invoice
            cart.save()
            print('processing purchase')
            cart.process_purchase()
        else:
            print('invalid payment')

    else:
        pass

@receiver(invalid_ipn_received)
def invalid_ipn(sender, **kwargs):
    print('invalid signal received')
