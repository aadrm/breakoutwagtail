# This Python file uses the following encoding: utf-8

from django import template
from django.urls import reverse # from django.urls for Django >= 2.0
from django.urls import resolve # from django.urls for Django >= 2.0
from django.utils import translation
from apps.wagtail.home.models import Page 

register = template.Library()

class TranslatedURL(template.Node):
    def __init__(self, language):
        self.language = language
    def render(self, context):
        view = resolve(context['request'].path)
        request_language = translation.get_language()
        translation.activate(self.language)
        page_id = context['page'].pk
        # print(view.url_name)
        # slug = Page.objects.get(pk=page_id).slug
        # print(slug)
        # view.args = (slug + '/', )
        # print(view.args)
        # print('tsthsnthsnothuesntoheua')
        # print(reverse(slug))
        # print(view.url_name, view.args, view.kwargs)
        url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        translation.activate(request_language)
        return url

@register.tag(name='translate_url')
def do_translate_url(parser, token):
    language = token.split_contents()[1]
    return TranslatedURL(language)