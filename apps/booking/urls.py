from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page


app_name = 'booking'


# handler404 = 'website.views.view_404'
urlpatterns = [
    # path('', views.booking_calendars, name='book'),
    
    path('slot_to_cart/', views.slot_to_cart, name='slot_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # path('coupons/', views.coupons, name='coupons'),
    path('purchase/', views.purchase, name='purchase'),
    path('order/<str:order>', views.order_completed, name='order'),

    path('add_product/', views.add_product, name='add_product'),
    path('add_product/<int:product_id>', views.add_product_by_id, name='add_product_by_id'),
    path('add_coupon/<str:coupon_code>/', views.add_coupon_by_code, name='add_coupon_by_code'),

    path('paypal_return/<str:cart>/<str:email>', views.paypal_return, name='paypal_return'),
    path('day_availability/', views.ajax_day_available_slots, name='ajax_day_availability'),

    path('pdf_coupon_code/', views.pdf_coupon_code, name='pdf_coupon_code'),
    path('pdf_coupon_code/<str:code>/', views.pdf_coupon_code, name='pdf_coupon_code'),

    path('calendar/', views.ajax_calendar, name='ajax_calendar'),
    path('ajax_admin_calendar/', views.ajax_admin_calendar, name='ajax_admin_calendar'),
    path('ajax_slot_booking/', views.ajax_slot_booking, name='ajax_slot_booking'),
    path('ajax_slot_disable/', views.ajax_slot_disable, name='ajax_slot_disable'),
    path('ajax_slot_enable/', views.ajax_slot_enable, name='ajax_slot_enable'),
    path('ajax_checkout_buttons/', views.ajax_checkout_buttons, name='ajax_checkout_buttons'),
    path('ajax_refresh_item/', views.ajax_refresh_item, name='ajax_refresh_item'),
    path('ajax_apply_coupon', views.ajax_apply_coupon, name='ajax_apply_coupon'),
    path('ajax_remove_coupon', views.ajax_remove_coupon, name='ajax_remove_coupon'),
    path('ajax_refresh_coupon', views.ajax_refresh_coupon, name='ajax_refresh_coupon'),
    path('ajax_refresh_invoice', views.ajax_refresh_invoice, name='ajax_refresh_invoice'),

    #admin extension views
    # path('appointments_list', views.appointments, name='appointments_list'),
    path('ajax_remove_coupon', views.ajax_remove_coupon, name='ajax_remove_coupon'),

    path('test_email_template/', views.test_email_template, name='test_email_template'),
    path('test_email_template/<str:mailto>', views.test_email_template, name='test_email_template'),
    path('test_email_template/<str:mailto>/<int:is_html_or_text>', views.test_email_template, name='test_email_template'),
    path('test_email_order/<str:order>', views.test_email_order, name='test_email_order'),
]
