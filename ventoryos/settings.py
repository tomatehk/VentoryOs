"""
Django settings for ventoryos project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vm^mx6p87e^e+h4(pmd693#4o5h0frqhka8_0o-n171g-#0vu%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'apps.section.apps.SectionConfig',
    'apps.shopping_cart.apps.ShoppingCartConfig',
    'apps.article.apps.ArticleConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'ventoryos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'apps/section/templates/jinja2'),
                 os.path.join(BASE_DIR, 'apps/article/templates/jinja2'),
                 os.path.join(BASE_DIR, 'apps/shopping_cart/templates/jinja2'),
                 os.path.join(BASE_DIR, 'apps/user/templates/jinja2'),
                 os.path.join(BASE_DIR, 'ventoryos/templates/jinja2'),
                 ],
        'OPTIONS': {
            'environment': 'ventoryos.jinja2.environment',
            'auto_reload': DEBUG,
            'autoescape': True,
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'ventoryos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ventoryos',
        'USER': 'postgres',
        'PASSWORD': 'storemg',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.' +
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

############## EMAIL ##############
# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS, EMAIL_POR estan configuradas para usar con gmail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com' # host smtp
EMAIL_HOST_USER = 'ventoryostest@gmail.com' # e-mail
EMAIL_HOST_PASSWORD = 'ventoryos1234' # contraseña
EMAIL_PORT = 587
############## EMAIL ##############
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Login Url
LOGIN_URL = '/user/login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
"Inportando la carpeta static en el projecto"

STATICFILES_DIRS = [
    "/home/brandom/workspace_ven/VentoryOs/ventoryos/static/"
]
