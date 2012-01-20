from django import forms

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
