from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random, name="random"),
    path("wiki/<str:page>/", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit_wiki/<str:page>/", views.edit_wiki, name="edit_wiki")
]
