from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginpage, name="login"),
    path("upload/", views.uploadpage, name="upload"),
    path("songs/", views.songs, name="songs")
]