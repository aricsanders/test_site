""" Views for a test site in django, django is assumed to be installed properly
"""
# Standard Imports
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from forms import *
from models import UploadFile,UploadFile2

# 3rd party Imports


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

@login_required
def FileView(request):
    if request.method == 'POST':
        form = UploadFileForm2(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(owner=request.user,file = request.FILES['file'])
            new_file.save()

            return HttpResponseRedirect(reverse('Files'))
    else:
        form = UploadFileForm()

    data = {'form': form}
    return render_to_response('file_template.html', data, context_instance=RequestContext(request))
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