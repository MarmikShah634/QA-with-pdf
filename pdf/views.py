import os
from django.http import HttpResponse
from django.shortcuts import render
import PyPDF2
from transformers import pipeline
import re
from pdf.forms import FileForm, QAForm

qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", tokenizer="bert-large-uncased-whole-word-masking-finetuned-squad")

def index(request):

    def detect_file_format(file_path):
        _, extension = os.path.splitext(file_path)
        if extension.lower() == '.pdf':
            return 'pdf'
        else:
            return 'Unknown'

    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

    def preprocess_text(text):
        text = re.sub(r'\s+', ' ', text)
        return text

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        pdf_path = "media/uploads/" + file_name
        text_from_pdf = extract_text_from_pdf(pdf_path)
        text_from_pdf = preprocess_text(text_from_pdf)
        request.session['text_from_pdf'] = text_from_pdf
        return render(request, 'qapdf.html')
    else:
        form = FileForm()
    return render(request, 'index.html', {'form': form})

def question_form(request):
    if request.method == 'POST':
        form = QAForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            question = question.lower()
            text_from_pdf = request.session.get('text_from_pdf')
            answer = qa_pipeline({'context': text_from_pdf, 'question': question})
            return HttpResponse("done")
    else:
        form = FileForm()
    return render(request, 'qapdf.html', {'form': form})
