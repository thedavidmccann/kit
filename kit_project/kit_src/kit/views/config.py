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

from ..forms import ConfigForm
from ..models import Config

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
