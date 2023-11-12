from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('landing/', views.landing, name='landing'), 
    path('myTrips/', views.myTrips, name='myTrips'), # type: ignore
    path('', views.getStarted, name='getStarted'),
]
