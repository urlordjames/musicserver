from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))

class SongUpload(forms.ModelForm):
    class Meta:
        model = models.Song
        fields = ["title", "privacy"]
    
    def __init__(self, *args, **kwargs):
        super(SongUpload, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["privacy"].widget.attrs.update({"class": "form-control"})