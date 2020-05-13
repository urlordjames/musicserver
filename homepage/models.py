from django.db import models

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    songfile = models.FileField(upload_to="songs/", max_length=50)