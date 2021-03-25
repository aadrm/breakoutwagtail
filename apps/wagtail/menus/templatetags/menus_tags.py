"""menus/templatetags/menus_tags.py"""
from django import template

from ..models import Menu, DocumentCollection
from wagtail.documents.models import Document

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.filter(slug=slug).first()

@register.simple_tag()
def get_documents(slug):
    return DocumentCollection.objects.filter(slug=slug).first()
    