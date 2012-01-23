from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models

import difflib

class ExcelContact(models.Model):

    email = models.EmailField()

    @classmethod
    def parse_name_xls(cls, value):
        return value.strip().title()

    @classmethod
    def process_phone_number_xls(cls, value, instance):
        # TODO add assign backend properly
        from rapidsms.models import Connection, Backend

        b, _ = Backend.objects.get_or_create(name='yo6700')
        c, _ = Connection.objects.get_or_create(identity=value.strip(), backend=b)
        c.contact = instance
        c.save()

    @classmethod
    def parse_reporting_location_xls(cls, value):
        from rapidsms.contrib.locations.models import Location

        try:
            toret = None
            model_names = Location.objects.values_list('name', flat=True)
            model_names_lower = [ai.lower() for ai in model_names]
            model_names_matches = difflib.get_close_matches(value.lower(), model_names_lower)
            if model_names_matches:
                toret = Location.objects.get(name__iexact=model_names_matches[0])
                return toret
        except Exception:
            raise ValidationError("Unknown location '%s'" % value)

    @classmethod
    def process_role_xls(cls, value, instance):
        name = value.strip().title()
        if value:
            group, _ = Group.objects.get_or_create(name=name)
            instance.groups.add(group)

    @classmethod
    def process_add_web_login_xls(cls, value, instance):
        if value.strip().lower() == 'yes':
            password = User.objects.make_random_password()
            u = User.objects.create_user(instance.email, instance.email, password)
            instance.user = u
            instance.save()
            send_mail('Your new login at kit.unicefuganda.org', "Your username is this email, your password is %s.\nEnjoy!\nUNICEF Uganda" % password, 'root@uganda.rapidsms.org', [instance.email], fail_silently=True)

    class Meta:
        abstract = True
