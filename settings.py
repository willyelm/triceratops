# Django settings for triceratops project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# specified in private_settings.py
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {}

TIME_ZONE = 'Europe/Jersey'
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'triceratops.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
)

# twitter users to syncronise with django
TWITTER_FOLLOW = (
    'rmjersey',
)

# import private settings, passwords etc. from outsite git repository scope
try:
    from private_settings import *
except ImportError:
    pass
