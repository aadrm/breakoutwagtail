from .models import FlexPage, InfoPage, FormPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from wagtail.contrib.forms.models import AbstractFormField

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



@register(FormPage)
class InfoPageTR(TranslationOptions):
    fields = (
        'intro',
        'content',
        'content_2',
        'thank_you_text',
        'subject',
        'submitted_title',
        'submitted_text',
    )
