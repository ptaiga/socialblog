from django.urls import path

from . import views

urlpatterns = [
    path('', views.ServerView.as_view())
]