from django.core.files import File
from django.core.exceptions import ValidationError
from django.db.transaction import commit_on_success
from django.forms.util import ErrorList

from poll.models import STARTSWITH_PATTERN_TEMPLATE

from xlrd import open_workbook

def parse_header_row(worksheet, model):
    """
    This method parses the top row of the spreadsheet for column names,
    introspecting the model for attributes, parse_attribute_xls() and 
    process_attribute_xls() methods, loading them into a list of typedefs per column.
    
    Each element in the list will contain a typedef dictionary:
    
    {'attribute_name':<attribute>,
     'has_attribute':True or False,
     'parse_method':bound method of model or None
     'process_method':None if 'has_attribute' is True, otherwise bound method of model
    }
    
    If has_attribute is False and no process method exists, a ValidationError will be thrown
    (likely this happens when the user has deleted the top row, the ValidationError
    will inform the user of such).
    """

    field_cols = []
    sample_instance = model()
    for col in range(worksheet.ncols):
        attribute = str(worksheet.cell(0, col).value).strip().lower().replace(" ", "_")
        if attribute:
            typedef = {'attribute_name':attribute, \
                       'has_attribute':False, \
                       'parse_method':None, \
                       'process_method':None}

            # look for parse_attribute_xls()
            parse_method = "parse_%s_xls" % attribute

            # look for process_attribute_xls()
            process_method = "process_%s_xls" % attribute

            if hasattr(model, parse_method):
                typedef['parse_method'] = getattr(model, parse_method)

            if attribute in dir(sample_instance):
                typedef['has_attribute'] = True

            if hasattr(model, process_method):
                typedef['process_method'] = getattr(model, process_method)

            if not (typedef['has_attribute'] or typedef['process_method']):
                raise ValidationError('Your upload encountered an unknown error.  Please ensure that the top row (column headings) is exactly as it was in the original template.')

            field_cols.append(typedef)

    return field_cols

@commit_on_success
def handle_excel_file(file, model, form):
    """
    This is the utility function that handles the actual uploading of each individual
    model instance.
    
    See the doc for kit.excel.upload.views.bulk_upload for the specific 
    processing rules, or the in-line documentation here for a more detailed
    explanation.
    """
    excel = file.read()
    try:
        workbook = open_workbook(file_contents=excel)
        worksheet = workbook.sheet_by_index(0)
    except:
        form.errors.setdefault('excel_file', ErrorList())
        form.errors['excel_file'].append("Please upload a valid excel file.")
        return

    try:
        attribute_typedef = parse_header_row(worksheet, model)
    except ValidationError, v:
        form.errors.setdefault('excel_file', ErrorList())
        form.errors['excel_file'].append(v.messages[0])
        return

    for row in range(1, worksheet.nrows):

        # this will be passed to model.objects.create()
        create_kwargs = {}

        for col in range(worksheet.ncols):
            value = str(worksheet.cell(row, col).value).strip().lower()
            typedef = attribute_typedef[col]
            attribute = typedef['attribute_name']

            if typedef['parse_method']:
                try:
                    create_kwargs[attribute] = typedef['parse_method'](value)
                except ValidationError, v:
                    form.errors.setdefault('excel_file', ErrorList())
                    form.errors['excel_file'].append("There was an error with row %d, column %s: %s" % (row, attribute, v.messages[0]))
                    continue
            elif typedef['has_attribute']:
                create_kwargs[attribute] = value
            else:
                # defer these calls to the second pass
                continue

        instance = model.objects.create(**create_kwargs)

        # second pass: call process_method() on all columns
        # that need it, passing in the above instance that was created
        for col in range(worksheet.ncols):
            value = str(worksheet.cell(row, col).value).strip().lower()
            typedef = attribute_typedef[col]
            attribute = typedef['attribute_name']

            if typedef['parse_method']:
                continue
            elif typedef['has_attribute']:
                continue
            else:
                try:
                    typedef['process_method'](value, instance)
                except ValidationError, v:
                    form.errors.setdefault('excel_file', ErrorList())
                    form.errors['excel_file'].append("There was an error with row %d, column %s: %s" % (row, attribute, v.messages[0]))
