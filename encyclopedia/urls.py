from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="details"),
    path("search", views.search, name="search"),
    path("addentry",views.addentry, name="addentry"),
    path("edit/<str:title>",views.editentry,name="editentry")
]