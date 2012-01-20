#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models import Q, Count
from django.views.decorators.http import require_GET
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, \
    render_to_response
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required, \
    permission_required
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.contrib import messages

from rapidsms.contrib.locations.models import Location
from rapidsms.models import Contact
from rapidsms_xforms.models import XFormField

def dashboard(req):

    return render_to_response('kit/dashboard.html',
                {'locations':Location.objects.all(),
                 'contacts':Contact.objects.all(),
                 'indicators':XFormField.objects.all()},
                context_instance=RequestContext(req))
