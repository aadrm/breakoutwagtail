from .base import *
from .system import *

DEBUG = False 

SECRET_KEY = config['SECRET_KEY']

ALLOWED_HOSTS = ['172.105.71.221', 'breakout-escaperoom.de']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config['DATABASE_NAME'],
        'USER': config['DATABASE_USER'],
        'PASSWORD': config['DATABASE_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}
PAYPAL_TEST = False
if PAYPAL_TEST:
    PAYPAL_IPN_POST_TO_ADDRESS = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
    PAYPAL_RECEIVER_EMAIL = 'sb-g47btr4711513@business.example.com'
else:
    PAYPAL_IPN_POST_TO_ADDRESS = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    PAYPAL_RECEIVER_EMAIL = 'info@breakout-escaperoom.de'

# Recaptcha
RECAPTCHA_PUBLIC_KEY = config['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = config['RECAPTCHA_PRIVATE_KEY']

try:
    from .local import *
except ImportError:
    pass
