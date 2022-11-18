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
        'NAME': 'cfd360_user',
        'USER': 'cfd360',
        'PASSWORD': 'RKzduwRNAORhspPck6jSFOIO8ciAafkg',
        'HOST': 'dpg-cdo4u19a6gdooi7q29v0-a',
        'PORT': '5432'
    }
}
"""