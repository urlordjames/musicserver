from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginpage, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("resetpassword/", views.passwordchange, name="resetpassword"),
    path("upload/", views.uploadpage, name="upload"),
    path("mymedia/", views.mymedia, name="mymedia"),
    path("publicmedia/", views.medialist, name="medialist"),
    path("player/", views.player, name="player"),
    path("getkey/", views.getkey, name="getkey"),
    path("edit/", views.edit, name="edit")
]