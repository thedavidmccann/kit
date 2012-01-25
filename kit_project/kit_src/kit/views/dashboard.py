#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from rapidsms.contrib.locations.models import Location
from rapidsms.models import Contact
from rapidsms_xforms.models import XFormField, XForm


def dashboard(req):

    return render_to_response('kit/dashboard.html',
                {'locations':Location.objects.all(),
                 'contacts':Contact.objects.all(),
                 'reports':XForm.objects.all(),
                 'indicators':XFormField.objects.all()},
                context_instance=RequestContext(req))
