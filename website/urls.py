from django.urls import path

from . import views


app_name = "website"

urlpatterns = [
    path("", views.page, name="home"),
    path("<path:page_path>/", views.page, name="page"),
]