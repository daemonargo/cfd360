from .base import *
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'cfd360.net', 'www.cfd360.net', 'cfd360.onrender.com']

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'defaultdb',
        'USER': 'doadmin',
        'PASSWORD': 'AVNS_Z9fBZWSJtbZo_8QMf65',
        'HOST': 'private-django-db-do-user-12720463-0.b.db.ondigitalocean.com',
        'PORT': '25060'
    }
}
"""