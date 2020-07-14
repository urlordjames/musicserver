import os
from threading import Thread
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password, ValidationError
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

def medialist(request):
    return render(request, "medialist.html", {"media": Song.objects.all().filter(privacy="public")})

@csrf_protect
def loginpage(request):
    if request.method == "GET":
        return render(request, "form.html", {"form": LoginForm(),
                                             "destination": "/login/",
                                             "action": "Login",
                                             "title": "Login"})
    elif request.method == "POST":
        loginform = LoginForm(request.POST)
        if not loginform.is_valid():
            messages.error(request, "login form invalid")
            return redirect("/login/")
        formdata = loginform.cleaned_data
        user = authenticate(request, username=formdata["username"], password=formdata["password"])
        if not user is None:
            login(request, user)
            messages.success(request, "you have successfully logged in!")
            return redirect("/")
        else:
            messages.error(request, "authentication failed")
        return redirect("/login/")
    else:
        return HttpResponse(status=405)

def logoutuser(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect("/")

@csrf_protect
def passwordchange(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            return render(request, "passwordreset.html")
        elif request.method == "POST":
            password = request.POST["password"]
            try:
                validate_password(password)
            except ValidationError as errors:
                for error in errors:
                    messages.error(request, error)
                return redirect("/resetpassword/")
            user.set_password(password)
            user.save()
            messages.success(request, "password changed")
            return redirect("/")  
        else:
            return HttpResponse(status=405)
    else:
        messages.error(request, "you are not logged in")
        return redirect("/login/")

@csrf_protect
def uploadpage(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "you are not logged in")
        return redirect("/login/")
    if request.method == "GET":
        return render(request, "form.html", {"form": SongUpload,
                                             "destination": "/upload/",
                                             "action": "Upload",
                                             "title": "Upload Media",
                                             "fileupload": True})
    elif request.method == "POST":
        if not user.is_superuser and len(Song.objects.all().filter(uploader=user)) >= 5:
            messages.error(request, "storage limit exceeded, delete your old media")
            return redirect("/mymedia/")
        uploadform = SongUpload(request.POST)
        if uploadform.is_valid():
            title = uploadform.cleaned_data["title"]
            templocation = os.path.join("temp", title + ".media")
            f = open(templocation, "wb+")
            for chunk in request.FILES["mediafile"]:
                f.write(chunk)
            f.close()
            data = uploadform.save(commit=False)
            data.uploader = user
            data.save()
            t = Thread(target=hlsify, args=(title, templocation))
            t.start()
            messages.success(request, "song successfully uploaded")
            return redirect("/mymedia/")
        messages.error(request, "upload form invalid")
        return redirect("/")
    else:
        return HttpResponse(status=405)

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

@csrf_protect
def edit(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    media = get_object_or_404(Song, title=request.GET.get("media"))
    if not media.uploader == request.user:
        return HttpResponse(status=401)
    if request.method == "GET":
        return render(request, "edit.html", {"media": media})
    elif request.method == "POST":
        if request.POST.get("delete") == "true":
            media.delete()
            messages.success(request, "deleted successfully")
            return redirect("/mymedia/")
        try:
            newprivacy = request.POST["privacy"]
        except KeyError:
            return HttpResponse(status=400)
        media.privacy = newprivacy
        media.save()
        messages.success(request, "edited successfully")
        return redirect("/mymedia/")
    else:
        return HttpResponse(status=405)