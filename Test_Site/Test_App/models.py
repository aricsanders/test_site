from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime
def get_date():
    """Returns todays date in 'yyyymmdd' format"""
    today=datetime.date.today()
    return today.strftime('%Y%m%d')
class UserExtension2(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.CharField('NIST Group', max_length=10)


class UserExtensionOnetoOne(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    agency = models.CharField('Agency', max_length=20, default='NIST')


class ProjectGroups(models.Model):
    people = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField('Group Name', max_length=20, default='')

    def __str__(self):
        out_string = self.name
        return out_string


class ProjectGroupsAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'


class ProjectGroups2(models.Model):
    class Meta:
        abstract=True
    name = models.CharField('Group Name', max_length=20, default='')
    def __str__(self):
        out_string = self.name
        return out_string

class ProjectG3(ProjectGroups2):
    pass



def generate_filename(self):
    today=datetime.date.today()
    url = "files/%s/%2d/%2d" % (today.year,today.month,today.day)
    return url

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    today=datetime.date.today()
    return 'files/{0}/{1}/{2}/{3}/{4}'.format(instance.owner.get_username(), today.year,today.month,today.day,filename)

class UploadFile(models.Model):
    owner=models.ForeignKey(User)
    file = models.FileField(upload_to=user_directory_path)
class UploadFile2(models.Model):
    file = models.FileField(upload_to=user_directory_path)

class UploadCanvas(models.Model):
    owner=models.ForeignKey(User)
    file = models.FileField(upload_to=user_directory_path)