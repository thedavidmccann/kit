from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from generic.sorters import SimpleSorter
from generic.views import generic
from rapidsms_xforms.models import XFormSubmission, XForm
from rapidsms_xforms.views import edit_submission

def edit_report(req, submission_id):
    submission = get_object_or_404(XFormSubmission, pk=submission_id)
    toret = edit_submission(req, submission_id)

    if type(toret) == HttpResponseRedirect:
        return redirect('/reports/%d/submissions/' % submission.xform.pk)
    else:
        return toret

def view_submissions(request, xform_pk):
    xform = get_object_or_404(XForm, pk=xform_pk)
    return generic(\
        request, \
        model=XFormSubmission, \
        queryset=xform.submissions.all().order_by('-created'), \
        objects_per_page=25, \
        base_template='kit/submissions_base.html', \
        partial_row='kit/partials/reports/submission_row.html', \
        results_title='Last Reporting Period Results', \
        columns=[('Reporter', True, 'message__connection__contact__name', SimpleSorter(),), \
                 ('Location', True, 'message__connection__contact__reporting_location__name', SimpleSorter(),), \
                 ('Report', True, 'raw', SimpleSorter(),), \
                 ('Date', True, 'created', SimpleSorter(),), \
                 ('Approved', True, 'approved', SimpleSorter(),), \
                 ('', False, '', None,)], \
        sort_column='message__connection__contact__healthproviderbase__healthprovider__facility__name', \
    )
