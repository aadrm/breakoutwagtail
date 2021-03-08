from datetime import datetime, time, timedelta
from apps.wagtail.site_settings.models import BookingSettings
from django.conf import settings
from wagtail.core.models import Site




def get_settings_site():
    return Site.objects.get(pk=settings.SITE_ID_FOR_SETTINGS)

def get_booking_settings():
    return BookingSettings.for_site(get_settings_site())

def addmins(tm, mins):
    """adds minutes to a datetime.time object"""
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, 0)
    fulldate = fulldate + timedelta(minutes=mins)
    return fulldate.time()
