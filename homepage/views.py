import os
from threading import Thread
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from .forms import LoginForm, SongUpload
from .models import Song
from .videoutils import hlsify, loadkey

def index(request):
    return render(request, "index.html", {"username": request.user.get_username()})

def mymedia(request):
    if request.user.is_authenticated:
        return render(request, "mymedia.html", {"media": Song.objects.all().filter(uploader=request.user)})
    else:
        messages.error(request, "you are not logged in")
        return redirect("/login/")

@csrf_protect
def loginpage(request):
    if request.method != "POST":
        return render(request, "form.html", {"form": LoginForm(),
                                             "destination": "/login/",
                                             "action": "Login",
                                             "title": "Login"})
    else:
        loginform = LoginForm(request.POST)
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
        return render(request, "form.html", {"form": SongUpload,
                                             "destination": "/upload/",
                                             "action": "Upload",
                                             "title": "Upload Media",
                                             "fileupload": True})
    else:
        uploadform = SongUpload(request.POST)
        if uploadform.is_valid():
            title = uploadform.cleaned_data["title"]
            templocation = os.path.join("temp", title + ".media")
            f = open(templocation, "wb+")
            for chunk in request.FILES["mediafile"]:
                f.write(chunk)
            f.close()
            data = uploadform.save(commit=False)
            data.uploader = request.user
            data.save()
            t = Thread(target=hlsify, args=(title, templocation))
            t.start()
            messages.success(request, "song successfully uploaded")
            return redirect("/mymedia/")
        messages.error(request, "upload form invalid")
        return redirect("/")

def player(request):
    return render(request, "player.html")

def getkey(request):
    requested = request.GET["media"]
    media = get_object_or_404(Song, title=requested)
    if media.privacy == "public":
        return HttpResponse(loadkey(requested), content_type="application/octet-stream")
    if request.user.is_authenticated:
        if media.uploader == request.user:
            return HttpResponse(loadkey(requested), content_type="application/octet-stream")
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=403)