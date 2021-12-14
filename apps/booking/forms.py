from django import forms
from django.core.validators import RegexValidator
from django.utils.html import format_html
from django.utils.translation import gettext as _

# from phonenumber_field.formfields import PhoneNumberField

from .models import Slot, Product, Invoice, Coupon, Room, Payment, PaymentMethod
from .utils import getProductsFromProductFamily
from paypal.standard.forms import PayPalPaymentsForm


class DateInput(forms.DateInput):
    input_type = 'date'

class SlotBookingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.slot_id = kwargs.pop('slot_id')
        self.slot = Slot.objects.get(pk=self.slot_id)

        super(SlotBookingForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(
            label=_('Players'),
            queryset=Product.objects.filter(family=self.slot.product_family),
        )
        self.fields['slot_id'] = forms.IntegerField(required=False, initial=self.slot_id) 


class InvoiceForm(forms.ModelForm):

    required_css_class = 'required'
    
    def __init__(self, *args, **kwargs):
        cart = kwargs.pop('cart')
        payment_methods = cart.get_valid_payment_methods()
        super().__init__(*args, **kwargs)
        self.fields['is_terms'].required = True
        self.fields['is_privacy'].required = True
        self.fields['phone'] = forms.CharField(label="phone", max_length=31, required=True)
        self.fields['payment'] = forms.ModelChoiceField(
            payment_methods,
            required=True,
            widget=forms.RadioSelect,
        )

    class Meta:
        model = Invoice
        fields = '__all__'


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.player_price_str()

class AddProductToCartForm(forms.Form):
    

    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', '')
        if family:
            products = family.products.all()
        else:
            products = Product.objects.all()
        super().__init__(*args, **kwargs)
        self.fields['product'] = MyModelChoiceField(
            products,
            required=True,
            # widget=forms.RadioSelect
        )


class RemoveFromCartForm(forms.Form):
    cart = forms.IntegerField(label='cart', required=True)
    item = forms.IntegerField(label='item', required=True)
    

class ApplyCouponForm(forms.Form):
    code = forms.CharField(label="code", max_length=32, required=True)


class CouponGeneratorForm(forms.ModelForm):

    # number = forms.IntegerField(_('Number of coupons'), required=False)

    class Meta:
        model = Coupon
        fields = [
            'name',
            'amount',
            'is_percent',
            'is_apply_to_basket',
            'is_individual_use',
            'is_overrule_individual_use',
            'is_upgrade',
            'product_families_included',
            'product_families_excluded',
            'product_included',
            'product_excluded',
            'use_limit',
            'expiry',
            'dow_valid',
        ]

    def __init__(self, *args, **kwargs):
        super(CouponGeneratorForm, self).__init__(*args, **kwargs)
        self.fields['number'] = forms.IntegerField(required=False)

    # def save(self, *args, **kwargs):
    #     times = self.cleaned_data['number']
    #     for i in range(0, times):
    #         super(CouponGeneratorForm, self).save(*args, **kwargs)
    # notes = forms.CharField(max_length='32', required=False)
    # amount = forms.DecimalField(required=False)
    # is_percent = forms.BooleanField(_('Apply as percent'), required=False)
    # is_apply_to_basket = forms.BooleanField(_('Apply to entire basket'), required=False)
    # is_individual_use = forms.BooleanField(_('Not compatible with coupons'), required=False)
    # is_overrule_individual_use = forms.BooleanField(_('Force compatibility with coupons'), required=False)
    # is_upgrade = forms.BooleanField(_('Upgrades the item'), required=False)
    # product_familie


class CustomPaypal(PayPalPaymentsForm):

    def render(self):
        return format_html(u"""<form action="{0}" method="post">

    {1}
    <button class="standard-button standard-button--emphasis"
    type="sumbit"  name="submit" />Pay Pal<button>
</form>""", self.get_endpoint(), self.as_p(), self.get_image())


class FilterAppointmentsForm(forms.Form):
    start_date = forms.DateField(widget=DateInput, required=False)
    end_date = forms.DateField(widget=DateInput, required=False)
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_active=True), required=False)
    search = forms.CharField(max_length=64, required=False)


class FilterOrdersForm(forms.Form):
    start_date = forms.DateField(widget=DateInput, required=False)
    end_date = forms.DateField(widget=DateInput, required=False)
    payment = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), required=False)
    search = forms.CharField(max_length=64, required=False)

class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Payment
        fields = ("invoice", "amount")
