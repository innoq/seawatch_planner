import os

import dj_database_url

from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(iyk95rqxz$r(dzj2=8g7d1e3ert=#730^i4*h7+m76s!o%9#6'

# Email Config
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {}
db_name = 'postgres'
db_user = 'postgres'
db_host = 'db'
db_port = 5432
DATABASES['default'] = \
    dj_database_url.config(default='postgres://' + db_user + ':@' + db_host + ':' + str(db_port) + '/' + db_name,
                           ssl_require=False)

ALLOWED_HOSTS = ['*']

NOSE_ARGS = ['--nocapture',
             '--nologcapture']

