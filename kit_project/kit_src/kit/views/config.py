#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..forms import ConfigForm
from ..models import Config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from rapidsms.contrib.locations.models import Location
from rapidsms.models import Contact, Backend, Connection
from rapidsms_xforms.models import XForm

@login_required
def edit_config(req):
    form = None

    if req.method == 'POST':
        form = ConfigForm(req.POST)
        if form.is_valid():
            for param in ['theme', 'brand']:
                c, _ = Config.objects.get_or_create(slug=param)
                c.value = form.cleaned_data[param]
                c.save()
    else:
        brand = 'unicef'
        theme = 'cyan'
        try:
            theme = Config.objects.get(slug="theme").value
        except Config.DoesNotExist:
            pass
        try:
            brand = Config.objects.get(slug="brand").value
        except Config.DoesNotExist:
            pass

        form = ConfigForm(initial={'brand':brand, 'theme':theme})

    return render_to_response('kit/config.html',
                {'form': form},
                context_instance=RequestContext(req))

@login_required
@transaction.commit_manually
def reset(req):
    try:
        User.objects.exclude(is_staff=True).delete()
        Group.objects.all().delete()
        Contact.objects.all().delete()
        XForm.objects.all().delete()
        Backend.objects.all().delete()
        Connection.objects.all().delete()
        Location.objects.all().delete()
        transaction.commit()
        return HttpResponse("The system has been reset", status=200)
    except:
        transaction.rollback()
