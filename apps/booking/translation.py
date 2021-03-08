from .models import (
    PaymentMethod,
    Product,
    Room,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(PaymentMethod)
class PaymentMethodTR(TranslationOptions):
    fields = (
        'name',
    )


@register(Product)
class ProductTR(TranslationOptions):
    fields = (
        'name',
    )


@register(Room)
class RoomTR(TranslationOptions):
    fields = (
        'description',
    )
