# -*- coding: utf-8 -*-

"""
Django settings for drf_poc project.

Generated by 'django-admin startproject' using Django 1.11.21.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-nbh6^g8e+juoc01ol%yyp0vw3a-+i@_@fl%t1=r**b)o+1c5&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'app02.apps.App02Config',
    'app03.apps.App03Config',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'mymiddleware.middleware.RobertMiddleware',
]

ROOT_URLCONF = 'drf_poc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'drf_poc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drf_poc',
        'USER': 'root',
        'PASSWORD': 'start01all',
        # 'HOST':'localhost',
        'HOST':'192.168.56.1',
        # To allow workmate visit the server in VM Ubuntu, Only Enable Bridget network And Disable the Host-Only network
        # 'HOST': '10.13.88.238',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(thread)d %(module)s %(lineno)d Line %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'drf_poc': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/drf_poc.log',
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html' : True,
        }
    },
    'loggers': {
        'drf_poc': {
            'handlers': ['console', 'drf_poc'],
            'level': 'INFO',
            'propagate': True,
        },
        # To print the sql in the python manage.py shell, Add the following logger
        # Of course you should also set the console handler level to DEBUG at the same time
        # 'django': {
        'django.db': {
            'handlers': ['console', 'drf_poc'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}
# Case 1: ???????????????????????? Bilibili ??? django rest framework ?????????
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES':(
#         'app01.utils.MyAllowAnyAuthentication','app01.utils.MyAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES':(
#         'app01.utils.MyPermission',
#     ),
#     'DEFAULT_THROTTLE_CLASSES': (
#         'app01.utils.VisitThrottle',
#     ),
#     'DEFAULT_THROTTLE_RATES': {
#         'general_rate':'5/m',
#         'vip_rate':'10/m',
#     },
#     # ??? URLPathVersioning ?????????, ????????? URL ?????????????????????
#     'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
#     'DEFAULT_VERSION':'v1',
#     'ALLOWED_VERSIONS':['v1', 'v2', 'v3'],
#     'VERSION_PARAM':'version',
#     # ?????????
#     'DEFAULT_PARSER_CLASSES':
#         ['rest_framework.parsers.JSONParser',
#          'rest_framework.parsers.FormParser',
#          'rest_framework.parsers.MultiPartParser'],
#     # ??????
#     'PAGE_SIZE':2,
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
# }
#
# Case 2: ???????????? archiver ?????? token ???????????????
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
}
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication