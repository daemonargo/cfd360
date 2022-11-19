from .base import *
#ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'cfd360.net', 'www.cfd360.net', 'cfd360.onrender.com', 'cfd360.herokuapp.com', 'www.cfd360.herokuapp.com']

DEBUG = True

"""if DEBUG == True:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
else:
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2u7n0iq6epklf',
        'USER': 'vnidaawijldlcr',
        'PASSWORD': '2c765c6776fd6d783696d8e2f982dd67a6ca22205086d78b7d45b42644c42955',
        'HOST': 'ec2-35-168-194-15.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
