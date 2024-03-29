from .base import *
# from .system import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY'] 
# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEV_THIRD_PARTY_APPS  = [
    'debug_toolbar',
]

DEV_MY_APPS = [

]

INSTALLED_APPS = INSTALLED_APPS + DEV_THIRD_PARTY_APPS + DEV_MY_APPS


PAYPAL_TEST = True
PAYPAL_IPN_POST_TO_ADDRESS = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
PAYPAL_RECEIVER_EMAIL = 'sb-g47btr4711513@business.example.com'

RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' 
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe' 
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


try:
    from .local import *
except ImportError:
    pass
