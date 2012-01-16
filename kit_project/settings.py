#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

# SMARTMIN CONFIG
# create the smartmin CRUDL permissions on all objects
#PERMISSIONS = {
#  '*': ('create', # can create an object
#        'read', # can read an object, viewing it's details
#        'update', # can update an object
#        'delete', # can delete an object,
#        'list'), # can view a list of the objects
#}

# assigns the permissions that each group should have, here creating an Administrator group with
# authority to create and change users
#GROUP_PERMISSIONS = {
#    "Administrator": ('auth.user.*',)
#}

# this is required by guardian
ANONYMOUS_USER_ID = -1

# set this if you want to use smartmin's user login
#LOGIN_URL = '/users/login'

import sys, os

filedir = os.path.dirname(__file__)
sys.path.append(os.path.join(filedir))
sys.path.append(os.path.join(filedir, 'rapidsms', 'lib'))
#sys.path.append(os.path.join(filedir, 'rapidsms_auth'))
#sys.path.append(os.path.join(filedir, 'rapidsms_contact'))
#sys.path.append(os.path.join(filedir, 'rapidsms_cvs'))
sys.path.append(os.path.join(filedir, 'rapidsms_generic'))
#sys.path.append(os.path.join(filedir, 'rapidsms_geoserver'))
sys.path.append(os.path.join(filedir, 'rapidsms_httprouter_src'))
sys.path.append(os.path.join(filedir, 'rapidsms_polls'))
#sys.path.append(os.path.join(filedir, 'rapidsms_script'))
#sys.path.append(os.path.join(filedir, 'rapidsms_uregister'))
sys.path.append(os.path.join(filedir, 'rapidsms_xforms_src'))
#sys.path.append(os.path.join(filedir, 'healthmodels'))
sys.path.append(os.path.join(filedir, 'django_eav'))
#sys.path.append(os.path.join(filedir, 'rapidsms_logistics'))
#sys.path.append(os.path.join(filedir, 'rapidsms_alerts'))
#sys.path.append(os.path.join(filedir, 'email_reports_src'))
#sys.path.append(os.path.join(filedir, '..', 'lib', 'dimagi-utils'))
#sys.path.append(os.path.join(filedir, 'rapidsms_uganda_common'))
#sys.path.append(os.path.join(filedir, 'rapidsms_uganda_ussd'))
#sys.path.append(os.path.join(filedir, 'rapidsms_unregister'))
sys.path.append(os.path.join(filedir, 'kit_src'))


# -------------------------------------------------------------------- #
#                          MAIN CONFIGURATION                          #
# -------------------------------------------------------------------- #
TIME_ZONE = "Africa/Kampala"
#ACTIVATION_CODE = 'start'
#OPT_IN_WORDS = ['join']
#OPT_OUT_WORDS = ['quit']

# map bounding box
MIN_LON = '29.5532'
MAX_LON = '33.9258'
MIN_LAT = '-1.0327'
MAX_LAT = '4.2807'
# map categorized color pallete
#CATEGORY_COLORS = ['#AA4643', '#4572A7', '#89A54E', '#80699B', '#3D96AE', '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92']

# you should configure your database here before doing any real work.
# see: http://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kit',
        'USER': 'postgres',
        'HOST': 'dbserver',
    }
}
# the rapidsms backend configuration is designed to resemble django's
# database configuration, as a nested dict of (name, configuration).
#
# the ENGINE option specifies the module of the backend; the most common
# backend types (for a GSM modem or an SMPP server) are bundled with
# rapidsms, but you may choose to write your own.
#
# all other options are passed to the Backend when it is instantiated,
# to configure it. see the documentation in those modules for a list of
# the valid options for each.
INSTALLED_BACKENDS = {
    "message_tester": {
        "ENGINE": "rapidsms.backends.bucket",
    },
}


# to help you get started quickly, many django/rapidsms apps are enabled
# by default. you may wish to remove some and/or add your own.
INSTALLED_APPS = [
#    "guardian",
#    "smartmin",
    "djtables",
    "mptt",
    "uni_form",

    "django_extensions",
    "django_digest",
    "django_nose",

#    "mtrack",
    "kit",
    "rapidsms",
    "rapidsms.contrib.handlers",
    "rapidsms.contrib.locations",
    "rapidsms.contrib.locations.nested",
    "rapidsms.contrib.default",

    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.humanize",

    "eav",
#    "healthmodels",
    "rapidsms_xforms",
#    "auth",
    "rapidsms_httprouter",
#    "script",
    "poll",
#    "cvs",
    "generic",
    "generic.reporting",
#    "geoserver",
#    "uganda_common",
#    "contact",
#    "logistics",
#    "email_reports",
#    "alerts",
#    "unregister",
#    "ussd",

    #Un/comment south in order to use South; also, for any apps
    # that you add to this list, all must be placed above "south"
#    "south",
]


SMS_APPS = [
    "mtrack",
    "cvs",
    "script",
    "poll",
    "rapidsms_xforms",
]

# this rapidsms-specific setting defines which views are linked by the
# tabbed navigation. when adding an app to INSTALLED_APPS, you may wish
# to add it here, also, to expose it in the rapidsms ui.
RAPIDSMS_TABS = [
    ("xforms", "Indicators"),
    ("polls", "Polls"),
]

AUTHENTICATED_TABS = [
#    ("polls", "Polls")
]

# -------------------------------------------------------------------- #
#                         BORING CONFIGURATION                         #
# -------------------------------------------------------------------- #


# debug mode is turned on as default, since rapidsms is under heavy
# development at the moment, and full stack traces are very useful
# when reporting bugs. don't forget to turn this off in production.
DEBUG = TEMPLATE_DEBUG = True


# after login (which is handled by django.contrib.auth), redirect to the
# dashboard rather than 'accounts/profile' (the default).
LOGIN_REDIRECT_URL = "/"


# use django-nose to run tests. rapidsms contains lots of packages and
# modules which django does not find automatically, and importing them
# all manually is tiresome and error-prone.
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

# for some reason this setting is blank in django's global_settings.py,
# but it is needed for static assets to be linkable.
MEDIA_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/media/"
# this is required for the django.contrib.sites tests to run, but also
# not included in global_settings.py, and is almost always ``1``.
# see: http://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1

# this is used for geoserver to tell which website this viz should be for (and prevents clashing of
# polls across different websites with the same id
DEPLOYMENT_ID = 5

# these weird dependencies should be handled by their respective apps,
# but they're not, so here they are. most of them are for django admin.
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
#    "logistics.context_processors.base_template",
#    "generic.context_processors.map_params",
    "kit.context_processors.skin",
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
)

# -------------------------------------------------------------------- #
#                           HERE BE DRAGONS!                           #
#        these settings are pure hackery, and will go away soon        #
# -------------------------------------------------------------------- #


# these apps should not be started by rapidsms in your tests, however,
# the models and bootstrap will still be available through django.
TEST_EXCLUDED_APPS = [
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rapidsms.contrib.ajax",
    "rapidsms.contrib.httptester",
]


TEMPLATE_LOADERS = (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.eggs.Loader'
)

# the project-level url patterns
ROOT_URLCONF = "urls"

#MAP_KEY = "ABQIAAAAmd7V71yw9ZddA0s8Z3wSKBS0unaJrFIrP1vn6ZXHpuhFyvYAGhQprSjp88j18w-K_X23JU31jBikVg"
#COUNTRY = "UG"
#MESSAGELOG_APP = 'rapidsms_httprouter'
#LOGISTICS_CONFIG = 'static.uganda.config'
#LOGISTICS_AGGRESSIVE_SOH_PARSING = False
#
#LOGISTICS_ALERT_GENERATORS = [
#    'logistics.alerts.non_reporting_facilities',
#    'logistics.alerts.facilities_without_reporters',
#    'logistics.alerts.facilities_without_reminders',
#]
#LOGISTICS_NOTIF_GENERATORS = [
#    'alerts._prototyping.notifiable_disease_test',
#    'alerts._prototyping.notiftest2',
#]
SYSTEM_USERNAME = '-mtrack-'

import os
import tempfile
import sys

try:
    import sys
    if os.environ.has_key('LOCAL_SETTINGS'):
        # the LOCAL_SETTINGS environment variable is used by the build server
        sys.path.insert(0, os.path.dirname(os.environ['LOCAL_SETTINGS']))
        from settings_test import *
    else:
        from localsettings import *
except ImportError:
    pass
# since we might hit the database from any thread during testing, the
# in-memory sqlite database isn't sufficient. it spawns a separate
# virtual database for each thread, and syncdb is only called for the
# first. this leads to confusing "no such table" errors. We create
# a named temporary instance instead.
if 'test' in sys.argv:
    for db_name in DATABASES:
        DATABASES[db_name]['TEST_NAME'] = os.path.join(
            tempfile.gettempdir(),
            "%s.rapidsms.test.sqlite3" % db_name)

