"""A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.
"""
from kit.models import Config

def skin(request):
    """
    a context processor that adds the main layout stylesheet to the 
    base layout of kit              
    """
    stylesheet = '/static/kit/stylesheets/themes/cyan/layout.css'
    try:
        c = Config.objects.get(slug='stylesheet')
        stylesheet = "/static/kit/stylesheets/themes/%s/layout.css" % c.value
    except Config.DoesNotExist:
        pass

    return {
        "layout_css":stylesheet
    }

