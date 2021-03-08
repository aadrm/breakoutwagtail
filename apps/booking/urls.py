from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page


app_name = 'booking'


# handler404 = 'website.views.view_404'
urlpatterns = [
    path('', views.booking_calendars, name='book'),
    path('calendar/', views.ajax_calendar, name='ajax_calendar'),
    
    path('slot_to_cart/', views.slot_to_cart, name='slot_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('coupons/', views.coupons, name='coupons'),
    path('purchase/', views.purchase, name='purchase'),
    path('order/<str:order>', views.order_completed, name='order'),

    path('add_product/', views.add_product, name='add_product'),

    path('test_paypal_ipn/', views.test_paypal_ipn, name='test_paypal_ipn'),
    path('day_availability/', views.ajax_day_available_slots, name='ajax_day_availability'),

    path('pdf_coupon_code/', views.pdf_coupon_code, name='pdf_coupon_code'),

    path('ajax_slot_booking/', views.ajax_slot_booking, name='ajax_slot_booking'),
    path('ajax_checkout_buttons/', views.ajax_checkout_buttons, name='ajax_checkout_buttons'),
    path('ajax_refresh_item/', views.ajax_refresh_item, name='ajax_refresh_item'),
    path('ajax_apply_coupon', views.ajax_apply_coupon, name='ajax_apply_coupon'),
    path('ajax_remove_coupon', views.ajax_remove_coupon, name='ajax_remove_coupon'),
    path('ajax_refresh_coupon', views.ajax_refresh_coupon, name='ajax_refresh_coupon'),
    path('ajax_refresh_invoice', views.ajax_refresh_invoice, name='ajax_refresh_invoice'),

    # path('ajax_slot_booking_test/', views.slot_booking_test, name='ajax_slot_booking_test'),
    path('calendartest/', views.ajax_calendar_test, name='ajax_calendar_test'),

    #admin extension views
    path('appointments_list', views.appointments, name='appointments_list'),
    path('coupon_generator', views.coupon_generator, name='coupon_generator'),
    path('ajax_remove_coupon', views.ajax_remove_coupon, name='ajax_remove_coupon'),

]
