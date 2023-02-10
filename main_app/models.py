from django.db import models

# Create your models here.

class PhotoContext(models.Model):
    date = models.DateField()
    description = models.TextField(max_length=500)

class Photo(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    photo_context = models.OneToOneField(PhotoContext, on_delete=models.CASCADE)