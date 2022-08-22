from django.contrib import admin
from django.urls import path, include

from viewer import views

urlpatterns = [
    path('', views.login_view, name="login_view"),
]
