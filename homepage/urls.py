from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginpage, name="login"),
    path("upload/", views.uploadpage, name="upload"),
    path("mymedia/", views.mymedia, name="mymedia"),
    path("player/", views.player, name="player"),
    path("getkey/", views.getkey, name="getkey")
]