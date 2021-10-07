from .settings import *

DATABASES = {
        'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'garage',
           'USER': 'postgres',
           'PASSWORD': 'example',
           'HOST': 'postgres',
           'PORT': '5432',
        }
    }
