import re
from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from wagtail.core.models import Site

from apps.wagtail.site_settings.models import BookingSettings


def get_booking_settings():
    settings = BookingSettings.objects.first()
    return settings

def booking_limit_date():
    now_date = timezone.now().date()
    # maximum limit is one year from now
    max_limit = now_date + timedelta(days=365)
    days = get_booking_settings().prevent_bookings_after_days
    date_limit = get_booking_settings().prevent_bookings_after_date

    # check if values are none
    if not days:
        days_limit = max_limit
    else:
        days_limit = now_date + timedelta(days=days)

    if not date_limit:
        date_limit = max_limit

    if days_limit < date_limit:
        return days_limit
    else:
        return date_limit
    




def addmins(tm, mins):
    """adds minutes to a datetime.time object"""
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, 0)
    fulldate = fulldate + timedelta(minutes=mins)
    return fulldate.time()

def textify(html):
    # Remove html tags and continuous whitespaces 
    soup = BeautifulSoup(html, "html.parser") # create a new bs4 object from the html data loaded
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text