from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . import forms

# Create your views here.

def index(request):
    return render(request, "index.html", {"username": request.user.get_username()})

@csrf_protect
def loginpage(request):
    if request.method != "POST":
        return render(request, "login.html", {"form": forms.LoginForm()})
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