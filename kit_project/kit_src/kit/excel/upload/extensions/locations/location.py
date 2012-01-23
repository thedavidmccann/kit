from django.core.exceptions import ValidationError
from django.db import models

class ExcelLocation(models.Model):

    code = models.CharField(max_length=50, unique=True, db_index=True)

    @classmethod
    def parse_name_xls(cls, value):
        return value.strip().title()

    @classmethod
    def parse_type_xls(cls, value):
        from rapidsms.contrib.locations.models import LocationType
        slug = value.strip().lower().replace(' ', '_')
        name = value.strip().title()
        toret, _ = LocationType.objects.get_or_create(slug=slug, name=name)
        return toret

    @classmethod
    def parse_code_xls(cls, value):
        from rapidsms.contrib.locations.models import Location

        code = value.strip().upper().replace(' ', '_')
        if Location.objects.filter(code=code).exists():
            raise ValidationError("Code '%s' already exists" % code)
        else:
            return code

    @classmethod
    def process_parent_code_xls(cls, value, instance):
        from rapidsms.contrib.locations.models import Location
        code = value.strip().upper().replace(' ', '_')

        if Location.objects.filter(code=code).exists():
            parent = Location.objects.get(code=code)
            instance.tree_parent = parent
            instance.save()

    class Meta:
        abstract = True
