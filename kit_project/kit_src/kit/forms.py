from django import forms
from django.contrib.auth.models import Group
from generic.forms import ActionForm
from mptt.forms import TreeNodeChoiceField
from rapidsms.models import Connection, Contact
from rapidsms_httprouter.models import Message
from rapidsms.contrib.locations.models import Location

class ConfigForm(forms.Form):
    # blue cyan grey green red
    theme = forms.ChoiceField(choices=[
                ('blue', 'Blue'),
                ('cyan', 'Cyan'),
                ('gray', 'Gray'),
                ('green', 'Green'),
                ('red', 'Red'),
            ], help_text="""
            This setting will add a theme to the elements of the header that are
            based on this color
            """)
    brand = forms.ChoiceField(choices=[
                ('unicef', 'UNICEF'),
                ('ugministry', 'Uganda Ministry of Health'),
            ],
            help_text="""
            Choose the heading logos that match your particular organization
            or project's needs.
            """)

class EditReporterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditReporterForm, self).__init__(*args, **kwargs)
        self.fields['reporting_location'] = \
            TreeNodeChoiceField(queryset=Location.tree.all(), level_indicator=u'.')
#            TreeNodeChoiceField(queryset=self.fields['reporting_location'
#                                ].queryset, level_indicator=u'.')


    class Meta:

        model = Contact
        fields = ('name', 'reporting_location', 'groups')


class EditLocationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditLocationForm, self).__init__(*args, **kwargs)
        self.fields['tree_parent'] = \
            TreeNodeChoiceField(queryset=Location.tree.all(), level_indicator=u'.')


    class Meta:

        model = Location
        fields = ('name', 'type', 'tree_parent')
