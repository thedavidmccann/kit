from django.db import models

class Config(models.Model):
    slug = models.SlugField(max_length=50, db_index=True,
                          help_text=u"Short unique attribute label", primary_key=True)
    value = models.CharField(max_length=100)


