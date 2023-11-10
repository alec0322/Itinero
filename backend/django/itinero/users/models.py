from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    

class User(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField()
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=20)

class State(models.Model):
    name = models.CharField(max_length=50)

class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class Trips(models.Model):
    TYPE_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    )

    typeOfTrip = models.CharField(max_length=50, choices=TYPE_CHOICES)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstDay = models.DateField()
    lastDay = models.DateField()

class Itinerary(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    date = models.DateField()
    hotel = models.CharField(max_length=50)

class Location(models.Model):
    name = models.CharField(max_length=100)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    time = models.TimeField()
