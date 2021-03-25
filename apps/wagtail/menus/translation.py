from modeltranslation.translator import register, TranslationOptions
from modeltranslation.decorators import register

from .models import MenuItem, Document

@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('link_title',)
    
@register(Document)
class DocumentTranslationOptions(TranslationOptions):
    fields = ('name',)