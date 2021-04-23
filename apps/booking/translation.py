from .models import (
    PaymentMethod,
    Product,
    Room,
    ProductFamily,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(ProductFamily)
class ProductFamilyTR(TranslationOptions):
    fields = (
        'name',
    )

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
