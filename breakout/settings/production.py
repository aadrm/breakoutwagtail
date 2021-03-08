from .base import *

DEBUG = False

SECRET_KEY = config['SECRET_KEY'] 

ALLOWED_HOSTS = ['173.105.71.221',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wagtaildjango',
        'USER': 'wagtaildjango',
        'PASSWORD': config['DATABASE_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}


try:
    from .local import *
except ImportError:
    pass
