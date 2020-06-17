from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import ffmpeg_streaming
from ffmpeg_streaming import Formats
import os
from .forms import LoginForm, SongUpload
from .models import Song

def index(request):
    return render(request, "index.html", {"username": request.user.get_username()})

def songs(request):
    return render(request, "songs.html", {"songs": Song.objects.all()})

@csrf_protect
def loginpage(request):
    if request.method != "POST":
        return render(request, "form.html", {"form": LoginForm(), "destination": "/login/", "action": "login"})
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
        return render(request, "form.html", {"form": SongUpload, "destination": "/upload/", "action": "upload", "fileupload": True})
    else:
        uploadform = SongUpload(request.POST, request.FILES)
        if uploadform.is_valid():
            title = uploadform.cleaned_data["title"]
            templocation = "temp/" + title + ".mp4"
            f = open(templocation, "wb+")
            for chunk in request.FILES["mediafile"]:
                f.write(chunk)
            f.close()
            video = ffmpeg_streaming.input(templocation)
            os.makedirs("media/" + title)
            hls = video.hls(Formats.h264())
            #TODO: put key into non-serving directory and add /getkey API
            hls.encryption("media/" + title + "/key", "/getkey?media=" + title)
            hls.auto_generate_representations()
            hls.output("media/" + title + "/" + "media.m3u8")
            data = uploadform.save(commit=False)
            data.uploader = request.user
            data.save()
            messages.success(request, "song successfully uploaded")
            return redirect("/")
        messages.error(request, "upload form invalid")
        return redirect("/")

def player(request):
    return render(request, "player.html")