from rapidsms_xforms.models import XForm, XFormField

def get_xform_list(request):
    toret = XForm.objects.all()
    if request.user.is_authenticated():
        if not request.user.is_staff:
            toret = toret.filter(restrict_to__in=request.user.groups.all())
        return toret

    return XForm.objects.none()

def get_xformfield_list(request):
    toret = XFormField.objects.filter(xform__active=True)
    if request.user.is_authenticated():
        if not request.user.is_staff:
            toret = toret.filter(xform__restrict_to__in=request.user.groups.all())
        return toret

    return XFormField.objects.none()

def check_user_xform_perms(user, xform):
    if user.is_staff:
        return True
    else:
        matches = set(user.groups.all()) & set(xform.restrict_to.all())

        # then the user must be part of at least one of the form's restricted groups
        return len(matches) > 0

    return False


def get_user_from_connection(connection):
    if connection.contact and connection.contact.user:
        return connection.contact.user
    return None



