from django import template

def get_submission_values(submission):
    return submission.eav.get_values().order_by('attribute__xformfield__order')

register = template.Library()
register.filter('get_submission_values', get_submission_values)
