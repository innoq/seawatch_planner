import dj_database_url
import django_heroku

from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(iyk95rqxz$r(dzj2=8g7d1e3ert=#730^i4*h7+m76s!o%9#6'

ALLOWED_HOSTS = ['*']

# Email Config
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Heroku Deploy
django_heroku.settings(locals(), databases=not DEBUG)

DATABASES = {}
db_name = 'postgres'
db_user = 'postgres'
db_host = 'db'
db_port = 5432
DATABASES['default'] = \
    dj_database_url.config(default='postgres://' + db_user + ':@' + db_host + ':' + str(db_port) + '/' + db_name,
                           ssl_require=False)

NOSE_ARGS = ['--nocapture',
             '--nologcapture']

DEBUG_PROPAGATE_EXCEPTIONS = True