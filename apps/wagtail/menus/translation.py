from modeltranslation.translator import register, TranslationOptions
from modeltranslation.decorators import register

from .models import MenuItem 

@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('link_title',)
    
