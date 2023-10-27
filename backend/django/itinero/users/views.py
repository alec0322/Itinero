from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import Post, User
from django.contrib.auth.hashers import check_password, make_password


def register(request):
    if request.method == 'POST':
        # Get data from the form
        password = make_password(request.POST['password'])
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please use a different email.")

        # Create a new User object and save it
        user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # You can add additional logic here, e.g., redirect to a login page
        return HttpResponse("User registered successfully.")
    else:
        # Render the registration form
        return render(request, 'users/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = None
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Authentication successful
                return HttpResponse("User Logged In successfully.")
            else:
                # Incorrect password
                return HttpResponse("Incorrect password.")
        except User.DoesNotExist:
            # User does not exist
            return HttpResponse("User does not exist.")


    else:
        # Render the login template
        return render(request, 'users/login.html')


def getStarted(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'users/getStarted.html')

def landing(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'users/landing.html')