from django.urls import path
from . import views

urlpatterns = [
    path('search_locations/', views.search_locations, name='search_locations'),
]