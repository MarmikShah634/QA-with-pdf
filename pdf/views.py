from django.shortcuts import render
import PyPDF2
from transformers import pipeline
import re

from pdf.forms import FileForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'qapdf.html')
    else:
        form = FileForm()
    return render(request, 'index.html', {'form': form})