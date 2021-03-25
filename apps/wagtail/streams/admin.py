from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)

from .models import Review, ReviewFamily, ReviewPlatform, Colour

class ReviewFamilyAdmin(ModelAdmin):
    model = ReviewFamily 
    menu_label = 'Review Family'
    menu_icon = 'placeholder'
    list_display = ('name',)


class ReviewPlatformAdmin(ModelAdmin):
    model = ReviewPlatform 
    menu_label = 'Platform'
    menu_icon = 'placeholder'
    list_display = ('name', 'score', 'link')

class ReviewAdmin(ModelAdmin):
    model = Review 
    menu_label = 'Review'
    menu_icon = 'placeholder'
    list_display = ('get_families', 'review')

class ColourAdmin(ModelAdmin):
    model = Colour 
    menu_label = 'Colour'
    menu_icon = 'placeholder'
    list_display = ('name', 'hex_code')
    menu_order = 202

class ReviewsGroup(ModelAdminGroup):
    menu_label = 'Reviews'
    menu_icon = 'placeholder'
    menu_order = 201
    items = (
        ReviewAdmin,
        ReviewPlatformAdmin,
        ReviewFamilyAdmin,
    )

modeladmin_register(ReviewsGroup)
modeladmin_register(ColourAdmin)