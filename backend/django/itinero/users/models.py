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