import re
from datetime import datetime, time, timedelta

from django.conf import settings
from django.utils.html import strip_tags
from wagtail.core.models import Site

from apps.wagtail.site_settings.models import BookingSettings


def get_booking_settings():
    settings = BookingSettings.objects.first()
    return settings 

def addmins(tm, mins):
    """adds minutes to a datetime.time object"""
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, 0)
    fulldate = fulldate + timedelta(minutes=mins)
    return fulldate.time()

def textify(html):
    # Remove html tags and continuous whitespaces 
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()