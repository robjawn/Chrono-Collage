from django.db import models

# Create your models here.

class PhotoContext(models.Model):
    date = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(max_length=500, blank=True, default='')
    location = models.CharField(max_length=200, blank=True, default='')
    people = models.CharField(max_length=200, blank=True, default='')

class Photo(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    photo_context = models.OneToOneField(PhotoContext, on_delete=models.CASCADE)