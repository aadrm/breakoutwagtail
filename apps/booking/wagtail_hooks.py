from django.urls import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem




@hooks.register('register_admin_menu_item')
def register_admin_menu_item():
  return MenuItem('Appointments', reverse('booking:appointments_list'), classnames='icon icon-folder-inverse', order=10000)

@hooks.register('register_admin_menu_item')
def register_coupon_generator_item():
  return MenuItem('Coupon Generator', reverse('booking:coupon_generator'), classnames='icon icon-folder-inverse', order=10001)
