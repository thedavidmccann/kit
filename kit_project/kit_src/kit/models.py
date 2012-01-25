from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from rapidsms_xforms.models import XForm, XFormField, XFormFieldConstraint

class Config(models.Model):
    slug = models.SlugField(max_length=50, db_index=True,
                          help_text=u"Short unique attribute label", primary_key=True)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s => %s" % (self.slug, self.value)


class Report(XForm):
    class Meta:
        proxy = True

    @classmethod
    def map_sms_keyword_xls(cls):
        return 'keyword'

    @classmethod
    def parse_owner_xls(cls, value):
        value = value.strip().lower()
        if User.objects.filter(username=value).exists():
            return User.objects.get(username=value)

        password = User.objects.make_random_password()
        u = User.objects.create_user(value, value, password)
        send_mail('Your new login at kit.unicefuganda.org', "Your username is this email, your password is %s.\nEnjoy!\nUNICEF Uganda" % password, 'root@uganda.rapidsms.org', value, fail_silently=True)
        return u

    @classmethod
    def process_role_xls(cls, value, instance):
        value = value.strip().title()
        if value:
            g, _ = Group.objects.get_or_create(name=value)
            instance.restrict_to.add(g)
            if not g in instance.owner.groups.all():
                instance.owner.groups.add(g)

        """
        Yep, turns out the role column doubles as a filthy hackish way to 
        hook into the xform instance and fix up the separator, keyword and
        command prefixes, and site.  Sorry.
        """
        instance.command_prefix = ''
        instance.keyword_prefix = ''
        instance.separator = ",;:*.\\s\""
        instance.site = Site.objects.get_current()
        instance.save()


class Indicator(XFormField):

    @classmethod
    def map_report_keyword_xls(cls):
        return 'xform'

    @classmethod
    def parse_xform_xls(cls, value):
        value = value.strip().lower()
        if XForm.objects.filter(keyword=value).exists():
            return XForm.objects.get(keyword=value)
        else:
            raise ValidationError("There is no report with keyword %s. Please upload it first" % value)

    @classmethod
    def map_indicator_keyword_xls(cls):
        return 'command'

    @classmethod
    def map_data_type_xls(cls):
        return "field_type"

    @classmethod
    def parse_field_type_xls(cls, value):
        value = value.strip().lower()
        map = { 'integer':XFormField.TYPE_INT, 'decimal':XFormField.TYPE_FLOAT, 'string':XFormField.TYPE_TEXT}
        if value in map:
            return map[value]
        else:
            raise ValidationError("Type must be one of integer, decimal, or string")

    @classmethod
    def process_required_value_xls(cls, value, instance):
        if value.strip().lower() == 'yes':
            XFormFieldConstraint.objects.create(type='req_val', field=instance, message="%s is required" % instance.name)

        # while we've got the instance, hook into it to fix some stuff up
        instance.type = instance.field_type
        fields = instance.xform.fields.order_by('-order')
        if fields.count() > 1:
            instance.order = fields[0].order + 1
        instance.save()

    class Meta:
        proxy = True

def cleanup_groups(sender, **kwargs):
    g = kwargs['instance']
    if kwargs['created']:
        for u in User.objects.filter(is_staff=True):
            u.groups.add(g)

post_save.connect(cleanup_groups, weak=True, sender=Group)
