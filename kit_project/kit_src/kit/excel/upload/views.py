#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError

from .forms import ExcelUploadForm
from .utils import handle_excel_file

@login_required
def bulk_upload(request, model=None, model_name=None, template=None, html_template='kit/excel/upload/upload.html'):
    """
    This is a generic view for uploading instances of a particular model
    in bulk.
    
    All the fields in the form are populated as attributes of the model and then
    one instance of the model is created per row.
    
    Consider the following example of a Model:
    
    class Inventory(models.Model):
        item = TextField()
        stock = IntegerField()
        
    And its bulk-uploaded spreadsheet:
    
    item     |  stock|
    ---------+-------|
    Apples   |     10|
    Oranges  |     20|
    
    This would result in two create() calls:
    
    >>> Inventory.objects.create(item='Apples', stock=10)
    >>> Inventory.objects.create(item='Oranges', stock=20)
    
    In the most simple case, a column will correspond exactly to what should
    be put in the database (for instance, a TextField that gets the string value
    of the cell, or an IntegerField that is coerced from a cell's string contents).
    
    In more complicated cases, a value may need a pre-processing step in order to
    coerce a cell into, for example, a foreign key.  For this case, this view will
    first search for a method in the Model called parse_<attribute>_xls(), where 
    <attribute> is the name of the attribute.  This parse method should accept a single
    argument, the string contents of the cell, and return the coerced object value 
    corresponding to this cell's contents (or throw a ValidationError).  If no such method
    is found, the view will attempt to coerce the cell contents directly.
    
    Another possibility is that a column name will need to be "friendly," but will
    actually map to an attribute with a more technical-sounding name 
    ('slug' being a great example of a not-user-friendly attribute!).  This view
    will also search for a method called map_<column>_xls(), which should return
    the name of the attribute this column should map to (as a string).  The view
    will then coerce the value from this column to the appropriate attribute, calling
    the parse method or coercing it directly.
    
    Finally, some spreadsheets may actually involve the creation of two models that
    may not be directly linked to the root model in a straightforward way.  In this 
    case, if neither a parse_<attribute>_xls method nor the attribute itself are
    found within the model, the view will attempt to call process_<attribute>_xls(),
    which will take in two arguments: the value of the cell, and the instance of 
    the base class that was created from the other columns in the row.
    This method should return nothing (or throw a ValidationError).
    
    If none of these attempts is successful, the view will throw an ImproperlyConfigured
    exception directly to Django.  
    """

    # model and template parameters are required
    if model is None or template is None:
        return HttpResponseServerError

    # set a sane default value for model_name, for display purposes.
    if model_name is None:
        model_name = model.__name__

    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_excel_file(request.FILES['excel_file'], model, form)

    else:
        form = ExcelUploadForm()

    return render_to_response(html_template, \
                              {'model_name':model_name, \
                               'form':form, \
                               'template':template, \
                               }, \
                              context_instance=RequestContext(request))
