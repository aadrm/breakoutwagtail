"""
Django settings for breakout project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
from pathlib import Path
from django.utils.translation import ugettext_lazy as _

try:
    with open('/etc/breakout_config.json') as config_file:
        config = json.load(config_file)
except Exception:
    with open('/sto/srv/breakoutdjango/breakout_config.json') as config_file:
        config = json.load(config_file)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    '192.168.178.27',
    # ...
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

DJANGO_CORE_APPS = [

    'mailer',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    "wagtail.contrib.table_block",
    'wagtail.contrib.settings',
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',
    'modeltranslation',
    'modelcluster',
    'taggit',
    'paypal.standard.ipn',
    'cookie_consent',
    'blog',
    'wagtail_svgmap',
    # 'django-crontab',
]

MY_APPS = [
    'apps.wagtail.flex.apps.FlexConfig',
    'apps.wagtail.site_settings.apps.SiteSettingsConfig',
    'apps.wagtail.streams.apps.StreamsConfig',
    'apps.wagtail.home.apps.HomePageConfig',
    'apps.wagtail.search',
    'apps.users.apps.UsersConfig',
    'apps.booking.apps.BookingConfig',
    'apps.wagtail.menus.apps.MenusConfig',
]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + MY_APPS

COOKIE_CONSENT_NAME = "cookie_consent"

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # should be after SessionMiddleware and before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'breakout.urls'
WAGTAIL_SVGMAP_IE_COMPAT: False
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'breakout.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# auth
AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = [
    ("en", "English"),
    ("de", "German"),
]

WAGTAIL_CONTENT_LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "breakout"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'
SITE_ID_FOR_SETTINGS = 2



# email setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'mailer.backend.DbBackend'
SERVER_EMAIL = 'info@breakout-escaperoom.de'
EMAIL_HOST = 'smtp.strato.de'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@breakout-escaperoom.de'
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True 



# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 578
# EMAIL_HOST_USER = 'breakout.augsburg@gmail.com'
# EMAIL_HOST_PASSWORD = 'RooM1006'
# EMAIL_USE_TLS = True 
# EMAIL_USE_SSL = False 

# EMAIL_HOST = 's191.goserver.host'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'web121p1'
# EMAIL_HOST_PASSWORD = 'peakADW-355'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

#paypal
PAYPAL_TEST = True
if PAYPAL_TEST:
    PAYPAL_IPN_POST_TO_ADDRESS = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
    PAYPAL_RECEIVER_EMAIL = 'sb-g47btr4711513@business.example.com'
else:
    PAYPAL_IPN_POST_TO_ADDRESS = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    PAYPAL_RECEIVER_EMAIL = 'info@breakout-escaperoom.de'