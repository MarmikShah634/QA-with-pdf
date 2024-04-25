from django.db import models

class FileModel(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class QAModel(models.Model):
    question = models.CharField(max_length=100)