from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']
PUBLIC_APPLICATION_URL = 'http://mcriscd01/childminder'
INTERNAL_IPS = "127.0.0.1"

# Base URL of notify gateway
NOTIFY_URL = 'http://notify-gateway:8000/notify-gateway'

# Base URL of payment gateway
PAYMENT_URL = 'http://payment-gateway:8000/payment-gateway'

# Base URL of arc-service gateway
ADDRESSING_URL = 'http://arc-service:8000/arc-service'

# Visa Validation
VISA_VALIDATION = False

DEV_APPS = [
    'debug_toolbar'
]

MIDDLEWARE_DEV = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': os.environ.get('DATABASE_USER', 'ofsted'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'OfstedB3ta'),
        'HOST': os.environ.get('DATABASE_HOST', 'ofsted-postgres'),
        'PORT': os.environ.get('DATABASE_PORT', '5432')
    }
}

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS

