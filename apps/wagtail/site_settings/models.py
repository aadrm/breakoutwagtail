from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.core import fields

from apps.wagtail.streams import blocks
# Create your models here.

@register_setting
class BookingSettings(BaseSetting):
    """booking settings"""
    slot_reservation_hold_minutes = models.IntegerField(blank=True, null=False, default=10)
    prevent_bookings_after_days = models.IntegerField(blank=True, null=False, default=90)
    prevent_bookings_after_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    slot_buffer_time = models.IntegerField(blank=True, null=True, default=2)
    booking_notification_emails = models.CharField(max_length=1024, null=True, blank=True)


    panels = [
        MultiFieldPanel(
            [
                FieldPanel("slot_reservation_hold_minutes"),
                FieldPanel("prevent_bookings_after_days"),
                FieldPanel("prevent_bookings_after_date"),
                FieldPanel("slot_buffer_time"),
                FieldPanel("booking_notification_emails"),
            ], 
        heading="Booking settings")
    ]
