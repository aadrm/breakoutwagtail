from .base import *

DEBUG = False

SECRET_KEY = config['SECRET_KEY'] 

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
