
from django import forms

from models import UploadFile


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadFile
        fields=['owner','file']
class UploadFileForm2(forms.ModelForm):

    class Meta:
        model = UploadFile
        fields=['file']

class UploadCanvasForm(forms.ModelForm):

    class Meta:
        model = UploadFile
        fields=['owner','file']

