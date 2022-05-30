from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.core import fields

from apps.wagtail.streams import blocks
# Create your models here.

@register_setting
class BookingSettings(BaseSetting):
    """booking settings"""
    slot_reservation_hold_minutes = models.IntegerField(
        blank=True,
        null=False,
        default=10
    )
    prevent_bookings_after_days = models.IntegerField(
        blank=True,
        null=False,
        default=90
    )
    prevent_bookings_after_date = models.DateField(
        help_text="Any slots after this date will not show in the calendar",
        auto_now=False,
        auto_now_add=False,
        blank=True, 
        null=True,
    )
    slot_buffer_time = models.IntegerField(
        help_text="Buffer time in minutes",
        blank=True,
        null=True,
        default=60
    )
    booking_notification_emails = models.CharField(
        help_text='Separate emails with a comma ","',
        max_length=1024,
        null=True,
        blank=True,
    )
    incentive_discount_adjacent_slots = models.IntegerField(
        help_text='Amount in EUR for the discount to be applied to slots close to other taken slots',
        default=0,
    )
    incentive_discount_parallel_slots = models.IntegerField(
        help_text='Amount in EUR for the discount to be applied to slots nexnextt to other taken slots',
        default=0,
    )


    panels = [
        MultiFieldPanel(
            [
                FieldPanel("slot_reservation_hold_minutes"),
                FieldPanel("prevent_bookings_after_days"),
                FieldPanel("prevent_bookings_after_date"),
                FieldPanel("slot_buffer_time"),
                FieldPanel("booking_notification_emails"),
                FieldPanel("incentive_discount_adjacent_slots"),
                FieldPanel("incentive_discount_parallel_slots"),
            ], 
        heading="Booking settings")
    ]
