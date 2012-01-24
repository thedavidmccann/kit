from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from generic.views import generic, generic_row
from generic.sorters import SimpleSorter
from kit.excel.upload.views import bulk_upload
from contact.forms import AssignGroupForm, MassTextForm
from contact.urls import urlpatterns as contact_urls
from kit.views import edit_config, dashboard, edit_reporter, delete_reporter, edit_location, delete_location
from rapidsms.contrib.locations.models import Location
from rapidsms.models import Contact
from rapidsms_xforms.models import XForm
from rapidsms_xforms.urls import urlpatterns as xform_urls
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
    url('^users/$', generic, { \
        'model':Contact, \
        'results_title':'Users', \
        'action_forms':[MassTextForm, AssignGroupForm], \
        'base_template':'kit/contacts_base.html',
        'partial_row':'kit/partials/contacts/contacts_row.html', \
        'columns':[ \
            ('Name', True, 'name', SimpleSorter()), \
            ('Number', True, 'connection__identity', SimpleSorter(),), \
            ('Location', True, 'reporting_location__name', SimpleSorter(),), \
            ('Role(s)', True, 'groups__name', SimpleSorter()), \
            ('', False, '', None)],
    }, name="kit-users"),
    url(r'^user/(?P<contact_pk>\d+)/edit', edit_reporter),
    url(r'^user/(?P<contact_pk>\d+)/delete', delete_reporter),
    url(r'^user/(?P<pk>\d+)/show', generic_row, {'model':Contact, 'partial_row':'kit/partials/contacts/contacts_row.html'}),

    url('^locations/$', generic, { \
        'model':Location, \
        'results_title':'Locations', \
        'base_template':'kit/locations_base.html',
        'partial_row':'kit/partials/locations/locations_row.html', \
        'columns':[ \
            ('Name', True, 'name', SimpleSorter()), \
            ('Type', True, 'type__name', SimpleSorter(),), \
            ('Parent', True, 'tree_parent__name', SimpleSorter(),), \
            ('', False, '', None)],
    }, name="kit-locations"),
    url(r'^location/(?P<location_pk>\d+)/edit', edit_location),
    url(r'^location/(?P<location_pk>\d+)/delete', delete_location),
    url(r'^location/(?P<pk>\d+)/show', generic_row, {'model':Location, 'partial_row':'kit/partials/locations/locations_row.html'}),

    url('^indicators/$', generic, {'model':XForm}, name="kit-indicators"),
    # RapidSMS contrib app URLs
    (r'^ajax/', include('rapidsms.contrib.ajax.urls')),
    (r'^export/', include('rapidsms.contrib.export.urls')),
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    (r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^scheduler/', include('rapidsms.contrib.scheduler.urls')),
    (r'^polls/', include('poll.urls')),
) + xform_urls + contact_urls

if settings.DEBUG:
    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
    )

#from rapidsms_httprouter.router import get_router
#get_router(start_workers=True)

