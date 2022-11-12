from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'defaultdb',
        'USER': 'doadmin',
        'PASSWORD': 'AVNS_Z9fBZWSJtbZo_8QMf65',
        'HOST': 'private-django-db-do-user-12720463-0.b.db.ondigitalocean.com',
        'PORT': '25060'
    }
}
