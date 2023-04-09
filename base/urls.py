from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('body/', views.body, name="body"),
]