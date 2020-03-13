"""
Django settings for rts project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&!ir31+b2wb_!426i%c*k=8%$syh7bc5c_%$!widorzmbd++@b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.rtscomics.com', 'localhost', '127.0.0.1']

# Site and SEO Information
SITE_NAME = 'RTS Comics'
META_KEYWORDS = 'Comics, Comix, Comics Books, Buy Comics'
META_DESCRIPTION = 'Comic collectors helping comic collectors since 1986. Your best source for comics.'
if DEBUG:
    SITE_URL = 'http://127.0.0.1:8000'
else:
    SITE_URL = 'https://rtscomics.com'
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
if not DEBUG:
    SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comix',
    'registration',
    'orders',
    'contact',
    'imports',
    'localflavor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'rts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rts_db',
            'USER': 'tim',
            'PASSWORD': 'rtsunl!mited',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wahhabb$default',
            'USER': 'wahhabb',
            'PASSWORD': 'c0ll%ns1',
            'HOST': 'wahhabb.mysql.pythonanywhere-services.com',
            'PORT': '',
        },
        'options': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
    MEDIA_ROOT = (os.path.join(BASE_DIR, "uploads"),)
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_all')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
    MEDIA_ROOT = (os.path.join(BASE_DIR, "uploads"),)

LOGIN_REDIRECT_URL = '/issues/'

# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'mail.rtsunlimited.com'
# EMAIL_HOST_USER = 'orders@rtsunlimited.com'
# EMAIL_HOST_PASSWORD = 's%P3#cj9V'
# DEFAULT_FROM_EMAIL = 'orders@rtsunlimited.com'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'wahhabb@gmail.com'
# EMAIL_HOST_PASSWORD = 'Goog2265^'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.lbcole.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'donotreply@lbcole.com'
EMAIL_HOST_PASSWORD = 'cxQ3&g274sz'

DEFAULT_FROM_EMAIL = 'donotreply@lbcole.com'

MANAGERS = (
    ('Webmaster', 'wahhab@deepwebworks.com'),
)

AUTH_PROFILE_MODULE = 'orders.userprofile'

if DEBUG:
    PAYPAL_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
else:
    PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'

PAYPAL_EMAIL = 'rtsunlimited@earthlink.net'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': SITE_ROOT + "/../data/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'comix': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'orders': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
    }
}