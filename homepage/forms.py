from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

class SongUpload(forms.ModelForm):
    class Meta:
        model = models.Song
        fields = ["songfile"]