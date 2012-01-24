from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from kit.forms import EditReporterForm
from rapidsms.models import Contact

@login_required
def delete_reporter(request, contact_pk):
    reporter = get_object_or_404(Contact, pk=contact_pk)
    if request.method == 'POST':
        reporter.delete()
    return HttpResponse(status=200)


@login_required
def edit_reporter(request, contact_pk):
    reporter = get_object_or_404(Contact, pk=contact_pk)
    reporter_form = EditReporterForm(instance=reporter)
    if request.method == 'POST':
        reporter_form = EditReporterForm(instance=reporter,
                data=request.POST)
        if reporter_form.is_valid():
            reporter_form.save()
        else:
            return render_to_response('kit/partials/contacts/edit_reporter.html'
                    , {'reporter_form': reporter_form, 'reporter'
                    : reporter},
                    context_instance=RequestContext(request))
        return render_to_response('kit/partials/contacts/contacts_row.html'
                                  , {'object'
                                  : Contact.objects.get(pk=contact_pk),
                                  'selectable': True},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('kit/partials/contacts/edit_reporter.html'
                                  , {'reporter_form': reporter_form,
                                  'reporter': reporter},
                                  context_instance=RequestContext(request))
