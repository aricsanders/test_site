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
import pandas
import math

# Constants
ONE_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\One_Port_Check_Standard.csv"
TWO_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Two_Port_Check_Standard.csv"
TWO_PORT_NR_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Two_Port_NR_Check_Standard.csv"
POWER_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Power_Check_Standard.csv"
COMBINED_ONE_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_One_Port_Check_Standard.csv"
COMBINED_TWO_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_Two_Port_Check_Standard.csv"
COMBINED_POWER_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_Power_Check_Standard.csv"
ONE_PORT_CALREP_CSV=r"C:\Share\Converted_DUT\One_Port_DUT.csv"
TWO_PORT_CALREP_CSV=r"C:\Share\Converted_DUT\Two_Port_DUT.csv"
POWER_3TERM_CALREP_CSV=r"C:\Share\Converted_DUT\Power_3Term_DUT.csv"
POWER_4TERM_CALREP_CSV=r"C:\Share\Converted_DUT\Power_4Term_DUT.csv"

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
def html_button_array(input_list,ncolumns=10):
    """Creates an array of buttons in an html table given a list"""
    nrows=math.ceil(float(len(input_list))/float(ncolumns))
    nrows=int(nrows)
    table_head="<table>"
    output=table_head
    for row in range(nrows):
        output=output+"<tr>"
        for column in range(ncolumns):
            if column+nrows*row<len(input_list):
                button_text='<td> <button class="btn btn-primary">{0}</button></td>'.format(input_list[column+nrows*row])
                output=output+button_text
            else:
                pass
        output=output+"</tr>"
    table_end="</table>"
    output=output+table_end
    return output
def html_anchor_array(input_list,ncolumns=10):
    """Creates an array of buttons in an html table given a list"""
    nrows=math.ceil(float(len(input_list))/float(ncolumns))
    nrows=int(nrows)
    table_head="<table>"
    output=table_head
    for row in range(nrows):
        output=output+"<tr>"
        for column in range(ncolumns):
            if column+nrows*row<len(input_list):
                href_text="/Test_App/CheckStandard/OnePort/{0}".format(input_list[column+nrows*row])
                button_text='<td> <a href="{0}">{1}</button></td>'.format(href_text,input_list[column+nrows*row])
                output=output+button_text
            else:
                pass
        output=output+"</tr>"
    table_end="</table>"
    output=output+table_end
    return output

@login_required
def checkstandard_view(request):
    """A view that shows checkstandard data"""
    try:
        one_port_data_frame=pandas.read_csv(COMBINED_ONE_PORT_CHKSTD_CSV)
        standards=one_port_data_frame["Device_Id"].unique()
        out_string=html_anchor_array(standards)
        if request.method == 'POST':
            form = UploadFileForm2(request.POST, request.FILES)
            if form.is_valid():
                new_file = UploadFile(owner=request.user,file = request.FILES['file'])
                new_file.save()
                new_registry_entry=UserFiles(owner=request.user,location=new_file.file.path,url=new_file.file.url)
                new_registry_entry.save()
                return HttpResponseRedirect(reverse('CheckStandard'))
        else:
            form = UploadFileForm()
        data = {'form': form, 'current_table':out_string}
        return render_to_response('checkstandard.html', data, context_instance=RequestContext(request))
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
        return render_to_response('checkstandard.html', data, context_instance=RequestContext(request))




@login_required
def FileView(request):
    try:
        current_file=UserFiles.objects.last()
        file_location=current_file.location
        os.chdir(TESTS_DIRECTORY)
        if file_location.split('.')[-1] in ['s2p']:
            table=S2PV1(current_file.location)
            xml=S2PV1_to_XMLDataTable(table)

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
            table=OnePortRawModel(file_location)
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