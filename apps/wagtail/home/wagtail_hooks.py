from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.core import hooks

@hooks.register("insert_global_admin_css", order=9000)
def global_admin_css():
    """add css to admin"""
    # return format_html('<link>')
    return format_html('<link rel="stylesheet" href={}>', static('css/custom_wagtail_admin.css'))