from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import FileModel, QAModel
from .forms import FileForm, QAForm  # Import your forms if necessary
import PyPDF2
from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pdfQA.settings")
setup()

def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

class YourAppTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_post(self):
        file_content = extract_text_from_pdf('media/uploads/marmikresume.pdf')
        uploaded_file = SimpleUploadedFile('test.pdf', file_content, content_type='application/pdf')
        response = self.client.post(reverse('index'), {'file': uploaded_file})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful POST

        # Assuming your models are ModelA and ModelB, you can check if the files were saved
        self.assertTrue(FileModel.objects.exists())
        self.assertTrue(QAModel.objects.exists())
        # Add more assertions if necessary

    def test_question_form_view_get(self):
        response = self.client.get(reverse('question_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qapdf.html')

    def test_question_form_view_post(self):
        file_content = extract_text_from_pdf('media/uploads/marmikresume.pdf')
        uploaded_file = SimpleUploadedFile('test.pdf', file_content, content_type='application/pdf')
        # Assuming you need to upload a file first before accessing the question_form
        self.client.post(reverse('index'), {'file': uploaded_file})

        # Assuming your form has a 'question' field
        response = self.client.post(reverse('question_form'), {'question': 'What is the question?'})
        self.assertEqual(response.status_code, 200)  # Assuming the question form always renders answer.html upon successful POST
        self.assertTemplateUsed(response, 'answer.html')
        # Add more assertions if necessary
