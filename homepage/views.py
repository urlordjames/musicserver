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
            return redirect("/login/")
        formdata = loginform.cleaned_data
        user = authenticate(request, username=formdata["username"], password=formdata["password"])
        if user != None:
            login(request, user)
            messages.success(request, "you have successfully logged in!")
            return redirect("/")
        else:
            messages.error(request, "authentication failed")
        return redirect("/login/")

@csrf_protect
def uploadpage(request):
    if not request.user.is_authenticated:
        messages.error(request, "you are not logged in")
        return redirect("/login/")
    if request.method != "POST":
        return render(request, "form.html", {"form": forms.SongUpload, "destination": "/upload/", "action": "upload"})
    else:
        uploadform = forms.SongUpload(request.POST, request.FILES)
        if uploadform.is_valid:
            data = uploadform.save(commit=False)
            data.uploader = request.user
            data.save()
            messages.success(request, "song successfully uploaded")
            return redirect("/")
        messages.error(request, "upload form invalid")
        return redirect("/")