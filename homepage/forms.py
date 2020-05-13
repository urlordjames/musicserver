from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput)
    password = forms.CharField(required=True, widget=forms.PasswordInput)