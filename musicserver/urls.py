from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from .settings import DEBUG

urlpatterns = [
    path("", include("homepage.urls")),
    path("upload/", include("homepage.urls")),
    path('admin/', admin.site.urls)
]

if DEBUG:
    urlpatterns += static("/media", document_root="./media")
    urlpatterns += static("/static", document_root="./static")