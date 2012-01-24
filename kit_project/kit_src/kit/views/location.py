from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from kit.forms import EditLocationForm
from rapidsms.contrib.locations.models import Location

@login_required
def delete_location(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)
    if request.method == 'POST':
        location.delete()
    return HttpResponse(status=200)


@login_required
def edit_location(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)
    location_form = EditLocationForm(instance=location)
    if request.method == 'POST':
        location_form = EditLocationForm(instance=location,
                data=request.POST)
        if location_form.is_valid():
            location_form.save()
            Location.tree.rebuild()
        else:
            return render_to_response('kit/partials/locations/edit_location.html'
                    , {'location_form': location_form, 'location'
                    : location},
                    context_instance=RequestContext(request))
        return render_to_response('kit/partials/locations/locations_row.html'
                                  , {'object'
                                  : Location.objects.get(pk=location_pk),
                                  'selectable': True},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('kit/partials/locations/edit_location.html'
                                  , {'location_form': location_form,
                                  'location': location},
                                  context_instance=RequestContext(request))
