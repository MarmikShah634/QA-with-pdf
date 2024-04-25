import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
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
            # Save the form data, including the file
            instance = form.save()
            
            # Access the saved file from the instance
            uploaded_file = instance.file
            file_name = uploaded_file.name
            pdf_path = "media/" + file_name
            
            # Perform further processing with the file
            text_from_pdf = extract_text_from_pdf(pdf_path)
            text_from_pdf = preprocess_text(text_from_pdf)
            
            # Store the processed text in the session
            request.session['text_from_pdf'] = text_from_pdf
            
            # Redirect to the desired page (e.g., qapdf.html)
            return redirect('question_form')
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
            return HttpResponse(answer['answer'])
    else:
        form = FileForm()
    return render(request, 'qapdf.html', {'form': form})
