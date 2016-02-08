""" Views for a test site in django, django is assumed to be installed properly
"""
# Standard Imports
from django.views.generic import TemplateView

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
class FileView(TemplateView):
    template_name='file_template.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context