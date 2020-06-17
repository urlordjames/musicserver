from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginpage, name="login"),
    path("upload/", views.uploadpage, name="upload"),
    path("songs/", views.songs, name="songs"),
    path("player/", views.player, name="player"),
    path("getkey/", views.getkey, name="getkey")
] + static("/media", document_root="./media")