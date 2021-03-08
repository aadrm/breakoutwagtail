from .models import FlexPage, InfoPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(FlexPage)
class FlexPageTR(TranslationOptions):
    fields = (
        'content',
    )

@register(InfoPage)
class InfoPageTR(TranslationOptions):
    fields = (
        'content',
    )
