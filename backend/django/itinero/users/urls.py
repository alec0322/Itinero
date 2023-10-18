from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('itinerary/', views.about, name='itinerary'),
    path('', views.home, name='home'),

    # other paths
]