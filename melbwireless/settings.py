# Django settings for melbwireless project.
import ConfigParser as configparser
import os
BASE_DIR = os.path.dirname(__file__)

mycnf = configparser.SafeConfigParser(defaults={
    'port': '',
})
mycnf.read(os.path.expanduser('~/.my.cnf'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Tyson Clugg', 'root+melbwireless@clugg.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'HOST': mycnf.get('mysql', 'host') or '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': mycnf.get('mysql', 'port') or '', # Set to empty string for default. Not used with sqlite3.
        'NAME': mycnf.get('mysql', 'database') or '', # Or path to database file if using sqlite3.
        'USER': mycnf.get('client', 'user') or '', # Not used with sqlite3.
        'PASSWORD': mycnf.get('client', 'password', raw=True) or '', # Not used with sqlite3.
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Melbourne'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1&m%$wd!v(&g8=vp%hiyk1hwdmg)a_3(3xz71ccf4e9h7g!cis'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "melbwireless.maps.context_processors.db",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'melbwireless.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'django_extensions',
    'leaflet',
    'melbwireless.maps',
    'melbwireless.oldsite',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'melbwireless.maps.models.UserManager',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
