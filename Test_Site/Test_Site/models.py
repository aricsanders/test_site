from django.db import models
from django.conf import settings
class UserExtension(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    group=models.CharField('NIST Group',max_length=10)
    