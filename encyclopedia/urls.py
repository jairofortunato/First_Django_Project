from django.urls import path

from . import views

from .views import entry

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_entry, name="new_entry"),
    path('random_entry/', views.random_entry, name='random_entry'),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),


]
