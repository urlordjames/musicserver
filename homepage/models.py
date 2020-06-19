import os
import shutil
from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def isfilesafe(string):
    if not string.isalpha():
        raise ValidationError("string is not alphanumeric")

def delfolder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

# Create your models here.

class Song(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[isfilesafe])

# recievers

@receiver(models.signals.pre_delete, sender=Song)
def nukefiles(sender, instance, **kwargs):
    delfolder(os.path.join("deployproxy", "media", instance.title))
    delfolder(os.path.join("keys", instance.title))