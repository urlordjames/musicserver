from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "index.html", {"cheezit": request.GET.get("dog")})

@csrf_protect
def loginpage(request):
    if request.method != "POST":
        return render(request, "login.html")
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user != None:
            login(request, user)
            messages.success(request, "you are logged in now!")
        else:
            messages.error(request, "authentication failed")
        return redirect("/")