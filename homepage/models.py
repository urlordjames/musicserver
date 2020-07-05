import os
import shutil
from string import ascii_letters
from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def isfilesafe(string):
    illegal = False
    safechars = ascii_letters + "1234567890 "
    for char in string:
        if not char in safechars:
            illegal = True
    if illegal:
        raise ValidationError("string is potentially unsafe")

def delfolder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

# Create your models here.

class Song(models.Model):
    privacyoptions = (
        ("private", "Private"),
        ("public", "Public")
    )

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[isfilesafe])
    privacy = models.CharField(max_length=20, choices=privacyoptions, default="private")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"

# recievers

@receiver(models.signals.pre_delete, sender=Song)
def nukefiles(sender, instance, **kwargs):
    delfolder(os.path.join("deployproxy", "media", instance.title))
    delfolder(os.path.join("keys", instance.title))