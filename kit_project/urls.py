from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
#from rapidsms_httprouter.urls import urlpatterns as router_urls
from rapidsms_xforms.urls import urlpatterns as xform_urls
from django.views.generic.simple import direct_to_template
from kit.views import edit_config, dashboard
from kit.excel.upload.views import bulk_upload
from rapidsms.contrib.locations.models import Location
from rapidsms.models import Contact
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^my-project/', include('my_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^users/', include('smartmin.users.urls')),
    (r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    (r'^account/', include('rapidsms.urls.login_logout')),
    url(r'^$', dashboard, name='rapidsms-dashboard'),
    url('^accounts/login', 'rapidsms.views.login'),
    url('^accounts/logout', 'rapidsms.views.logout'),
    url('^config/$', edit_config),
    url('^config/locations/$', bulk_upload, {'model':Location, 'template':'/static/kit/spreadsheets/locations_tmpl.xls'}, name='upload-locations'),
    url('^config/users/$', bulk_upload, {'model':Contact, 'model_name':'User', 'template':'/static/kit/spreadsheets/users_tmpl.xls'}, name='upload-contacts'),
    # RapidSMS contrib app URLs
    (r'^ajax/', include('rapidsms.contrib.ajax.urls')),
    (r'^export/', include('rapidsms.contrib.export.urls')),
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    (r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^scheduler/', include('rapidsms.contrib.scheduler.urls')),
    (r'^polls/', include('poll.urls')),
) + xform_urls

if settings.DEBUG:
    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
    )

#from rapidsms_httprouter.router import get_router
#get_router(start_workers=True)

