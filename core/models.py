from django.db import models

# Create your models here.

class Image(models.Model):
    image=models.ImageField(upload_to='images/')
    def __str__(self):

        return str(self.pk)

class Trans(models.Model):
    col1 = models.TextField(max_length=20)
    col2 = models.TextField(max_length=20)
    def __str__(self):
        return str(self.pk)
    