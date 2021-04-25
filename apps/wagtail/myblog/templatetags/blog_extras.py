import html
from django import template
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator

register = template.Library()

@register.filter(name='excerpt')
def excerpt_with_ptag_spacing(value, arg):

    try:
        limit = int(arg)
    except ValueError:
        return 'Invalid literal for int().'

    # remove spaces between tags
    value = strip_spaces_between_tags(value)

    # add space before each P end tag (</p>)
    value = value.replace("</p>"," </p>")
    value = value.replace("</h2>"," </h2>")
    value = value.replace("</h3>"," </h3>")
    value = value.replace("</h4>"," </h4>")
    value = value.replace("</h5>"," </h5>")
    value = value.replace("</h6>"," </h6>")


    # strip HTML tags
    value = strip_tags(value)
    # other usage: return Truncator(value).words(length, html=True, truncate=' see more')
    return html.unescape(Truncator(value).words(limit))