from django.urls import reverse, path
from wagtail.core import hooks
from wagtail.contrib.modeladmin.menus import MenuItem, Menu, SubmenuMenuItem

from . import views



# Submenu

breakout_menu = Menu('register_breakout_item')
breakout_submenu = SubmenuMenuItem(label="Breakout", order=101, menu=breakout_menu, classnames='icon icon-folder')

@hooks.register('construct_main_menu')
def add_breakout_menu(request, menu_items):
    menu_items.insert(0, breakout_submenu)


# Sumbmenu items


@hooks.register('register_breakout_item')
def register_coupon_generator_item():
  return MenuItem('Orders', reverse('orders_list'), classnames='icon icon-fa-shopping-basket', order=10001)

@hooks.register('register_breakout_item')
def register_admin_menu_item():
  return MenuItem('Appointments', reverse('appointments_list'), classnames='icon icon-fa-calendar-check-o', order=100)

@hooks.register('register_breakout_item')
def register_coupon_generator_item():
  return MenuItem('Payments', reverse('payments'), classnames='icon icon-fa-credit-card', order=10001)

@hooks.register('register_breakout_item')
def register_coupon_generator_item():
  return MenuItem('Coupons to ship', reverse('shipping'), classnames='icon icon-fa-truck', order=10001)

@hooks.register('register_breakout_item')
def register_coupon_generator_item():
  return MenuItem('Coupon Generator', reverse('coupon_generator'), classnames='icon icon-fa-industry', order=10001)



# URLS

@hooks.register('register_admin_urls')
def urlconf_time():
  return [
    path('appointments_list', views.appointments, name='appointments_list'),
    path('orders_list', views.order_summary, name='orders_list'),
    path('shipping', views.shipping, name='shipping'),
    path('coupon_generator', views.coupon_generator, name='coupon_generator'),
    path('payments', views.record_payment, name='payments'),
  ]
  from django import urls
