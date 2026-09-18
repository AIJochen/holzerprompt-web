from django.urls import path

from . import views


app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:language_prefix>/", views.home, name="localized_home"),
]