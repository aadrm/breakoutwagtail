from paypal.standard.models import ST_PP_COMPLETED, ST_PP_PENDING
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import PaymentMethod, Invoice, Payment
from .cart.models import Cart
from .forms import InvoiceForm
from .utils import send_cart_emails
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
        price = cart.total

        payment = PaymentMethod.objects.get(method='paypal')
        invoice = cart.invoice
        if invoice:
            invoice.full_name=ipn_obj.first_name + ' ' + ipn_obj.last_name
            invoice.phone=ipn_obj.contact_phone
            invoice.street=ipn_obj.address_street
            invoice.post=ipn_obj.address_zip
            invoice.city=ipn_obj.address_city
            invoice.is_terms=True
            invoice.is_privacy=True
        else:
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

        print(invoice.__dict__)
        print(invoice.full_name, type(invoice.full_name))
        print(invoice.phone, type(invoice.phone))
        print(invoice.street, type(invoice.street))
        print(invoice.post, type(invoice.post))
        print(invoice.city, type(invoice.city))
        print(invoice.is_terms, type(invoice.is_terms))
        print(invoice.is_privacy, type(invoice.is_privacy))
        invoice.save()
        cart.invoice = invoice
        cart.save()
        payment = Payment(invoice=cart.invoice, amount=ipn_obj.mc_gross)
        payment.save()

        print('processing purchase')
        cart.process_purchase()
        send_cart_emails(cart)

    else:
        pass

@receiver(invalid_ipn_received)
def invalid_ipn(sender, **kwargs):
    print('invalid signal received')
