import pyclbr
import re
from django.contrib import admin
from .models import UserExtension
admin.site.register(UserExtension)
# def register_all_models(module=None,path=None):
#     """ This function registers all modules in with the django admin.
#     The module name should be a string, and defaults to 'models' and the path can be a string, list or tuple"""
#     if module is None:
#         module='.models'
#     if path is None:
#         classes = pyclbr.readmodule(module)
#     elif type(path) is str:
#         classes = pyclbr.readmodule(module,[path])
#     else:
#         classes = pyclbr.readmodule(module,path)
#     for model in classes:
#         # now the dirty part, check that the models are classes that inherit from models.Model
#         # if this inhertance is not explicit in the class call it will not be registered
#         for superclass in classes[model].super:
#             if re.search('models.Model',superclass):
#                 # this could be a from module import * above this loop
#                 exec('from %s import %s'%(module,classes[model].name))
#                 exec('admin.site.register(%s)'%classes[model].name)
#
# register_all_models('models',[r'C:\Users\sandersa\Test_Site\Test_Site'])
