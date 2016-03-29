""" Views for a test site in django, django is assumed to be installed properly
"""
# Standard Imports
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from .forms import *
from .models import *
import re
# 3rd party Imports
from pyMeasure.Code.DataHandlers.GeneralModels import *
from pyMeasure.Code.DataHandlers.NISTModels import *
from pyMeasure.Code.DataHandlers.TouchstoneModels import *
from pyMeasure.Code.DataHandlers.Translations import *

# Constants

# Functions

# Classes

# The easiest view is just subclassing a Template View, the context is supplied by caputuring pieces of the url
class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

# class FileView(TemplateView):
#     template_name='file_template.html'


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
def FileView(request):
    try:
        current_file=UserFiles.objects.last()
        file_location=current_file.location
        os.chdir(TESTS_DIRECTORY)
        if file_location.split('.')[-1] in ['s2p']:
            table=S2PV1(current_file.location)
            xml=S2PV1_to_XMLDataTable(table,**{"style_sheet":"../XSL/S2P_STYLE_02.xsl"})

        elif file_location.split('.')[-1] in ['s1p']:
            table=S1PV1(current_file.location)
            xml=S1PV1_to_XMLDataTable(table,**{"style_sheet":"../XSL/S1P_STYLE.xsl"})

        elif file_location.split('.')[-1]==file_location and re.search('_',file_location):
            table=JBSparameter(file_location)
            old_prefix=table.get_frequency_units().replace('Hz','')
            table.change_unit_prefix(column_selector=0,old_prefix=old_prefix,new_prefix='G',unit='Hz')
            table.column_names=S2P_RI_COLUMN_NAMES
            xml=AsciiDataTable_to_XMLDataTable(table,**{"style_sheet":"../XSL/S2P_STYLE_02.xsl"})

        elif file_location.split('.')[-1] in ['asc','txt'] and not re.search('raw',file_location,re.IGNORECASE):
            table=OnePortModel(file_location)
            xml=AsciiDataTable_to_XMLDataTable(table)

        elif file_location.split('.')[-1] in ['txt'] and re.search('raw',file_location,re.IGNORECASE):
            table=OnePortRawModel(file_location)
            xml=AsciiDataTable_to_XMLDataTable(table,**{"style_sheet":"../XSL/ONE_PORT_RAW_STYLE.xsl"})

        out_string=xml.to_HTML()
        if request.method == 'POST':
            form = UploadFileForm2(request.POST, request.FILES)
            if form.is_valid():
                new_file = UploadFile(owner=request.user,file = request.FILES['file'])
                new_file.save()
                new_registry_entry=UserFiles(owner=request.user,location=new_file.file.path,url=new_file.file.url)
                new_registry_entry.save()


                return HttpResponseRedirect(reverse('Files'))
        else:
            form = UploadFileForm()
        data = {'form': form, 'current_table':out_string}
        return render_to_response('file_template.html', data, context_instance=RequestContext(request))
    except:
        out_string="\n<b>You Have Broken It</b> "
        if request.method == 'POST':
            form = UploadFileForm2(request.POST, request.FILES)
            if form.is_valid():
                new_file = UploadFile(owner=request.user,file = request.FILES['file'])
                new_file.save()
                new_registry_entry=UserFiles(owner=request.user,location=new_file.file.path,url=new_file.file.url)
                new_registry_entry.save()


                return HttpResponseRedirect(reverse('Files'))
        else:
            form = UploadFileForm()
        data = {'form': form, 'current_table':out_string}
        return render_to_response('file_template.html', data, context_instance=RequestContext(request))



@csrf_protect
@login_required
def CanvasView2(request):
    if request.method == 'POST':
        form = UploadFileForm2(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(owner=request.user,file = request.FILES['file'])
            new_file.save()

            return HttpResponseRedirect(reverse('Canvas2'))
    else:
        form = UploadFileForm()

    data = {'form': form}
    return render_to_response('canvas_template2.html', data, context_instance=RequestContext(request))


class CanvasView(TemplateView):
    template_name='canvas_template.html'
# def CanvasView(request):
#     if request.method == 'POST':
#         form = UploadCanvasForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_file = UploadFile(owner=request.user,file = request.FILES['file'])
#             new_file.save()
#
#             return HttpResponseRedirect(reverse('Canvas'))
#     else:
#         form = UploadCanvasForm()
#
#     data = {'form': form}
#     return render_to_response('canvas_template.html', data, context_instance=RequestContext(request))