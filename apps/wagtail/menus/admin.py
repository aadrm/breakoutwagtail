from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup

from .models import WagtailLanguage

# Register your models here.

class WagtailLanguageAdmin(ModelAdmin):
    model = WagtailLanguage 
    menu_label = 'languages'
    menu_icon = 'placeholder'
    menu_order = 900
    list_display = ('language_code',)

modeladmin_register(WagtailLanguageAdmin)