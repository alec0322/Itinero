from django.db import models
from users.models import User
import json

class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state}"

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

    def __str__(self):
        return f"{self.typeOfTrip} Trip to {self.city.name}"

class Itinerary(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    hotel_list = models.TextField()
    hotel = models.CharField(max_length=250) #need to change to only hold the index of the list of places
    
    def set_hotel_list(self, hotel_list):
        self.hotel_list = json.dumps(hotel_list)

    def get_hotel_list(self):
        return json.loads(self.hotel_list)

class Location(models.Model):
    TIME_SLOT_CHOICES = (
        (1, 'Breakfast'),
        (2, 'Mid-Day Activity'),
        (3, 'Lunch'),
        (4, 'Evening Activity'),
        (5, 'Dinner'),
    )

    name = models.CharField(max_length=150)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=50, choices=TIME_SLOT_CHOICES)
    activity = models.CharField(max_length=100)
    search_keyword = models.CharField(max_length=150, default='')
    place = models.CharField(max_length=200)  # or models.ForeignKey(Place, on_delete=models.CASCADE)
    place_list = models.TextField()  # or models.ManyToManyField(Place)
    
    def set_places(self, place_list):
        self.place_list = json.dumps(place_list)

    def get_places(self):
        return json.loads(self.place_list)