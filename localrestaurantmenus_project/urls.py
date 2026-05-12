"""Root URL configuration."""
from django.urls import path

from localrestaurantmenus_project import views

urlpatterns = [
    path("", views.home, name="home"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("<slug:slug>/", views.restaurant, name="restaurant"),
]
