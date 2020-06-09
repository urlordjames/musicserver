from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def isfilesafe(string):
    if not string.isalpha():
        raise ValidationError("string is not alphanumeric")

# Create your models here.

class Song(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, validators=[isfilesafe])