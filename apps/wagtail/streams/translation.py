from .models import (
    Review
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Review)
class ReviewTR(TranslationOptions):
    fields = (
        'review',
    )

