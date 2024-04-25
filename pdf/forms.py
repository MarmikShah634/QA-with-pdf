from django import forms
from .models import FileModel, QAModel

class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file']

class QAForm(forms.ModelForm):
    class Meta:
        model = QAModel
        fields = ['question']