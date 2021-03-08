from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = 'apps.booking'

    def ready(self):
        print('importing hooks')
        from .handlers import show_me_the_money
        from .handlers import invalid_ipn
