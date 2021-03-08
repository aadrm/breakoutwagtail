from .base import *

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

try:
    from .local import *
except ImportError:
    pass
