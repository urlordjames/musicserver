from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.text import slugify
from . import forms

def index(request):
    return render(request, "index.html", {"username": request.user.get_username()})

@csrf_protect
def loginpage(request):
    if request.method != "POST":
        return render(request, "form.html", {"form": forms.LoginForm(), "destination": "/login/", "action": "login"})
    else:
        loginform = forms.LoginForm(request.POST)
        if not loginform.is_valid():
            messages.error(request, "login form invalid")
            return redirect("/")
        formdata = loginform.cleaned_data
        user = authenticate(request, username=formdata["username"], password=formdata["password"])
        if user != None:
            login(request, user)
            messages.success(request, "you have successfully logged in!")
        else:
            messages.error(request, "authentication failed")
        return redirect("/")

#TODO: refactor so the upload is in the app I labeled "upload" but then proceeded to not put the upload stuff in because I'm an idiot
@csrf_protect
def uploadpage(request):
    if request.method != "POST":
        return render(request, "form.html", {"form": forms.SongUpload, "destination": "/upload/", "action": "upload"})
    else:
        uploadform = forms.SongUpload(request.POST, request.FILES)
        if not uploadform.is_valid:
            messages.error(request, "upload form invalid")
            return redirect("/")
        #WARNING! POTENTIALLY UNSAFE CODE!!!
        f = open(request.FILES["songfile"].name, "wb")
        for chunk in request.FILES["songfile"].chunks():
            f.write(chunk)
        f.close()
        messages.success(request, "song successfully uploaded")
        return redirect("/")