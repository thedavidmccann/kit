from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from rapidsms_xforms.models import XForm

class Config(models.Model):
    slug = models.SlugField(max_length=50, db_index=True,
                          help_text=u"Short unique attribute label", primary_key=True)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s => %s" % (self.slug, self.value)


class Report(XForm):
    class Meta:
        proxy = True


def cleanup_groups(sender, **kwargs):
    g = kwargs['instance']
    if kwargs['created']:
        for u in User.objects.filter(is_staff=True):
            u.groups.add(g)

post_save.connect(cleanup_groups, weak=True, sender=Group)
