from django.urls import path
from . import views

app_name = "My Back Yard"
urlpatterns = [
    path('', views.home, name="home"),
]
