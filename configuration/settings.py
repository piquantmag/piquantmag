import os
import logging.config

import markdown

from django.http import Http404
from django.utils.log import DEFAULT_LOGGING
from django.utils.translation import gettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')

ENVIRONMENT = os.getenv('STAGE', 'dev')
IS_DEVELOPMENT = ENVIRONMENT == 'dev'
IS_STAGING = ENVIRONMENT == 'staging'
IS_PRODUCTION = ENVIRONMENT == 'production'
IS_CI = os.getenv('CI', False) == 'true'
DEBUG = IS_DEVELOPMENT or IS_CI

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

SITE_ID = 1
SITE_NAME = 'Piquant'

BUILTIN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'webpack_loader',
    'markupfield',
    'ordered_model',
    'storages',
]

MY_APPS = [
    'communication',
    'zine',
    'about',
    'styleguide',
]

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROLLBAR = {
    'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
    'environment': ENVIRONMENT,
    'root': BASE_DIR,
    'exception_level_filters': [
        (Http404, 'ignored'),
    ],
    'handler': 'blocking',
    'patch_debugview': False,
}

ROOT_URLCONF = 'configuration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.template_visible_settings',
            ],
        },
    },
]

TEMPLATE_VISIBLE_SETTINGS = [
    'ENVIRONMENT',
    'FACEBOOK_APP_ID',
    'DEFAULT_PAGE_DESCRIPTION',
    'IS_PRODUCTION'
]

WSGI_APPLICATION = 'configuration.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', 3306),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'CONN_MAX_AGE': 300,
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

STATICFILES_DIRS = [
    ASSETS_DIR,
]

if IS_PRODUCTION or IS_STAGING:
    STATICFILES_STORAGE = 'configuration.storages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'configuration.storages.MediaStorage'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

BUCKET_PREFIX = os.getenv('BUCKET_PREFIX')

MEDIA_BUCKET_NAME = f'{BUCKET_PREFIX}-media-{ENVIRONMENT}'
MEDIA_DOMAIN = f'media-{ENVIRONMENT}.piquantmag.com'
MEDIA_URL = '/media/' if DEBUG else f'https://{MEDIA_DOMAIN}/'

STATIC_BUCKET_NAME = f'{BUCKET_PREFIX}-static-{ENVIRONMENT}'
STATIC_DOMAIN = f'static-{ENVIRONMENT}.piquantmag.com'
STATIC_URL = '/static/' if DEBUG else f'https://{STATIC_DOMAIN}/'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_IS_GZIPPED = True

ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')

DEFAULT_PAGE_DESCRIPTION = _(
    'A publication dedicated to uncovering culture, history, traditions, and secrets about the food we eat every day.'
)

FACEBOOK_APP_ID = '1424778977620660'

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

MARKUP_FIELD_TYPES = (
    ('markdown', markdown.markdown),
)

LOGGING_CONFIG = None
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGERS = {
    '': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'django.server': DEFAULT_LOGGING['loggers']['django.server']
}
LOGGERS.update({
    app: {
        'level': LOG_LEVEL,
        'handlers': ['console'],
        'propagate': False,
    } for app in MY_APPS
})
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server']
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server']
    },
    'loggers': LOGGERS,
})

SECURE_SSL_REDIRECT = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31_536_000
