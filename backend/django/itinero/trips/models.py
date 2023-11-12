from django.db import models
from users.models import User

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
    date = models.DateField()
    hotel = models.CharField(max_length=50)

class Location(models.Model):
    TIME_SLOT_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('mid_day', 'Mid-Day Activity'),
        ('lunch', 'Lunch'),
        ('evening', 'Evening Activity'),
        ('dinner', 'Dinner'),
    )

    name = models.CharField(max_length=100)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    time = models.TimeField()
    time_slot = models.CharField(max_length=50, choices=TIME_SLOT_CHOICES)
    activity = models.CharField(max_length=50)
    search_keyword = models.CharField(max_length=50)
    place = models.CharField(max_length=200)  # or models.ForeignKey(Place, on_delete=models.CASCADE)
    places = models.TextField()  # or models.ManyToManyField(Place)