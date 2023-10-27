from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from .models import Post, User


def register(request):
    if request.method == 'POST':
        # Get data from the form
        password = make_password(request.POST['password'])
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
            return render(request, 'users/register.html', {'error_message': error_message, 'email': email, 'first_name': first_name, 'last_name': last_name})

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
        error_message = None

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Authentication successful
                # Redirect to the landing page
                return HttpResponseRedirect(reverse('landing'))
            else:
                # Incorrect password
                error_message = "Incorrect password."
        except User.DoesNotExist:
            # User does not exist
            error_message = "User does not exist."

        # Render the login template with the error message
        return render(request, 'users/login.html', {'error_message': error_message})

    else:
        # Render the login template without an error message
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