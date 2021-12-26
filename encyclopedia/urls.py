from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("q", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("savepage", views.savepage, name="savepage"),
    path("changepage/<str:title>", views.changepage, name="changepage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage")
]
