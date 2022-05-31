from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)

from . import views
from .models import (Cart, CartCoupon, CartItem, Coupon, Invoice, Payment,
                     PaymentMethod, Product, ProductFamily, Room, Schedule,
                     Slot)


class TabularInlineCartItems(admin.TabularInline):
    model = CartItem
    exclude = ['coupon', 'cart_coupons', 'marked_shipped']
    extra = 0

class TabularInlineCartCoupons(admin.TabularInline):
    model = CartCoupon
    extra = 0
    
# Register your models here.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    exclude = ['slot', 'cart_coupons',]

@admin.register(CartCoupon)
class CartCouponAdmin(admin.ModelAdmin):
    pass 

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('pk','name','code','amount')
    list_filter = ('name', 'created')
    search_fields = ['code', 'name']
    

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'start_date', 'end_date', 'start_time', 'end_time')


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    list_display = ('start', 'room')    
    list_filter = ('room',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'family')
    pass 

@admin.register(ProductFamily)
class ProductFamilyAdmin(admin.ModelAdmin):
    pass 

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [TabularInlineCartItems, TabularInlineCartCoupons]

    def get_urls(self):
        urls = super(CartAdmin, self).get_urls()
        my_urls = [
            url(r'^change_slot_list/$', self.admin_site.admin_view(views.change_slot_list), name='change_slot_list'),
            url(r'^change_slot/$', self.admin_site.admin_view(views.change_slot), name='change_slot'),
            url(r'^change_product_list/$', self.admin_site.admin_view(views.change_product_list), name='change_product_list'),
            url(r'^change_product/$', self.admin_site.admin_view(views.change_product), name='change_product'),
            url(r'^delete_order/$', self.admin_site.admin_view(views.delete_order), name='delete_order'),
        ]
        return my_urls + urls

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(PaymentAdmin, self).get_urls()
        my_urls = [
            url(r'^record_payment/$', self.admin_site.admin_view(views.record_payment), name='record_payment'),
        ]
        return my_urls + urls
    
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass
    
# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'code',)

#     def get_urls(self):
#         urls = super(CouponAdmin, self).get_urls()
#         my_urls = [
#             url(r'^generator/$', self.admin_site.admin_view(views.coupon_generator), name='coupon_generator')
#         ]
#         return my_urls + urls


class ProductFamilyAdmin(ModelAdmin):
    model = ProductFamily 
    menu_label = 'Product Families'
    menu_icon = 'fa-object-group'
    list_display = ('pk', 'name', 'payment_methods', 'room')


class ProductAdmin(ModelAdmin):
    model = Product 
    menu_label = 'Products'
    menu_icon = 'fa-object-ungroup'
    list_display = ('pk', 'family', 'name', 'price')


class CouponAdmin(ModelAdmin):
    model = Coupon 
    search_fields = ['code']
    menu_label = 'Coupons'
    menu_icon = 'fa-envelope'

    list_display = ('pk', 'name', 'code')


class RoomAdmin(ModelAdmin):
    model = Room 
    menu_label = 'Rooms'
    menu_icon = 'fa-film'
    list_display = ('name', 'is_active')


class ScheduleAdmin(ModelAdmin):
    model = Schedule
    menu_label = 'Calendar Schedule'
    menu_icon = 'fa-calendar'
    list_display = ('pk', '__str__', 'start_date', 'end_date', 'start_time', 'end_time')
    menu_order = 1


class AppointmentsGroup(ModelAdminGroup):
    menu_label = 'Rooms Setup'
    menu_icon = 'fa-calendar-check-o'
    menu_order = 200
    items = (
        ProductFamilyAdmin,
        ProductAdmin,
        CouponAdmin,
        ScheduleAdmin,
        RoomAdmin,
    )

modeladmin_register(AppointmentsGroup)


# from apps.wagtail.streams.models import Review 

# class ReviewAdmin(ModelAdmin):
#     model = Review 
#     menu_label = 'Review'
#     menu_icon = 'placeholder'
#     list_display = ('family', 'review')


# class ReviewsGroup(ModelAdminGroup):
#     menu_label = 'Reviews'
#     menu_icon = 'placeholder'
#     menu_order = 201
#     items = (
#         ReviewAdmin
#     )

# modeladmin_register(ReviewsGroup)