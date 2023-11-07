from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('landing/', views.landing, name='landing'),
    path('', views.getStarted, name='getStarted'),
    path('pastTrips/', views.pastTrips, name='pastTrips'),

    # other paths
]