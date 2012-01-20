from django.db import models

class ExtendedContact(models.Model):

    def total_submissions(self):
        from rapidsms_xforms.models import XFormSubmission
        return XFormSubmission.objects.filter(connection__in=self.connection_set.all(), has_errors=False).count()

    class Meta:
        abstract = True
