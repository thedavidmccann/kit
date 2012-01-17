from django import forms

class ConfigForm(forms.Form):
    # blue cyan grey green red
    theme = forms.ChoiceField(choices=[
                ('blue', 'Blue'),
                ('cyan', 'Cyan'),
                ('grey', 'Grey'),
                ('green', 'Green'),
                ('red', 'Red'),
            ])
    brand = forms.ChoiceField(choices=[
                ('unicef', 'UNICEF'),
                ('ugministry', 'Uganda Ministry of Health'),
            ])
