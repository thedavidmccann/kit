from django import forms

class ExcelUploadForm(forms.Form):

    excel_file = forms.FileField(\
        label='Excel File', \
        help_text='Upload your completed excel spreadsheet here.', \
        required=True)
