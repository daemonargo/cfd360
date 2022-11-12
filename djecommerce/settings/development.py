from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'cfd360.net', 'www.cfd360.net', 'cfd360.onrender.com', 'www.cfd360.onrender.com']
#ALLOWED_HOSTS = ['*']
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
