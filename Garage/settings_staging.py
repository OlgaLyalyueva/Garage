import os

from Garage.settings import *  # noqa F403
from Garage.settings import SECRET_KEY

DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = os.getenv(SECRET_KEY,
                       '+xk4lbvirpc5l0!bz=3$h@m7jbpy=2x=qfof8-g7*v99cime#5')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Garage',
        'USER': 'garage_s',
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT', default=15432),
    }
}
