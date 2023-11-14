from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, User
from trips.models import Trips, City, State, Location, Itinerary
from trips.scripts.place_recommender import *
from trips.views import recommend_view
from django.contrib import messages
from django.core.exceptions import ValidationError
import random
from datetime import datetime, timedelta


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

        # Add a success message
        messages.success(request, "Congratulations! You've registered successfully! Login now to begin creating your itinerary.")

        # Redirect to the homepage
        return redirect('getStarted')  # Replace 'homepage' with the name of your homepage URL pattern

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
                request.session['user_id'] = user.id  # type: ignore
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
        # Render the login template
        return render(request, 'users/login.html')


def getStarted(request):
    return render(request, 'users/getStarted.html')


def landing(request):
    # Check if a user is logged in by checking if their ID is in the session
    user_id = request.session.get('user_id')
    
    if user_id:
        user = User.objects.get(pk=user_id)  # Retrieve the user using their ID

        # Your existing code to handle landing page when a user is logged in
        if request.method == 'POST':
            cityState = request.POST.get('cityStateInput')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            try:
                # Split the string into city and state using the comma as a delimiter
                city_name, state_name = map(str.strip, cityState.split(','))
            except ValueError:
                return render(request, 'users/landing.html', {'error_message': 'Please Fill Out All Fields'})

            # Convert city and state to lowercase
            city_name = city_name.lower()

            try:
                # Retrieve the state and city from the database
                state = State.objects.get(name=state_name)
                city = City.objects.get(name=city_name, state=state)

                # Create a new Trips object
                trip = Trips(
                    typeOfTrip='upcoming',
                    city=city,
                    user=user,
                    firstDay=start_date,
                    lastDay=end_date,
                )

                try:
                    trip.save()
                    
                    # # Get the ID of the saved trip
                    # trip_id = trip.id

                    places = recommendPlace(str(city), "hotel", '8000')
                    if places:
                        rand = random.randrange(10)
                        hotel_place = places[rand]

                    # Create a new Itinerary object
                    itinerary = Itinerary(
                        hotel=hotel_place,  # selected hotel
                        trip_id=trip.id
                    )
                    itinerary.set_hotel_list(places)
                    
                    # Save the Itinerary object to the database
                    itinerary.save()
                    
                    # Convert date strings to datetime.date objects
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    # Calculate the number of days between start_date and end_date
                    day_count = (end_date - start_date).days + 1
                    event_list = {
                        1: "Breakfast",
                        2: "Midday Activity",
                        3: "Lunch",
                        4: "Evening Activity",
                        5: "Dinner"
                    }
                    
                    for i in range(day_count):
                        for x in range(1, 6):
                            places = recommendPlace(str(city), event_list.get(x), '8000')
                            place = random.choice(places)
                            date = start_date + timedelta(days=i)   #instead of time this really means day :/
                            time_slot = x
                            activity = event_list.get(x) 
                            search_keyword = ''
                            
                            location = Location(
                            name=place['name'],                 # name of place
                            itinerary=itinerary,             # itinerary id
                            date=date,                          # date of trip
                            time_slot=time_slot,                # 1 of 5 events of day used for ordering
                            activity=activity,                  # Default secondary search keyword
                            search_keyword=search_keyword,      # Primary search keyword
                            place=place,               # Place selected
                        )
                            location.set_places(places)             # Saving places list to json for future callbacks
                            location.save()

          
                except ValidationError:
                    return render(request, 'users/landing.html', {'error_message': 'Invalid date format. Please enter a date in the format YYYY-MM-DD.'})

                # Pass to the template
                itin = {
                    'trip': trip,
                    'itinerary': itinerary,
                    'location': location,
                }
                    
                return render(request, 'users/itinerary.html', itin)

            except (State.DoesNotExist, City.DoesNotExist):
                return render(request, 'users/landing.html', {'error_message': 'City not found in the database.'})

        else:
            # Render the landing page with the form
            return render(request, 'users/landing.html')

    else:
        # Handle the case when the user is not logged in (not in session)
        return render(request, 'users/login.html', {'error_message': 'Please log in to start.'})


def myTrips(request):
    # Check if a user is logged in by checking if their ID is in the session
    user_id = request.session.get('user_id')
    
    if user_id:
        user1 = User.objects.get(pk=user_id)  # Retrieve the user using their ID
        # Fetch the user's trips
        user_trips = Trips.objects.filter(user=user1)

        # Split trips into upcoming and past based on the end date
        current_date = timezone.now().date()
        upcoming_trips = [trip for trip in user_trips if trip.lastDay >= current_date]
        past_trips = [trip for trip in user_trips if trip.lastDay < current_date]

        # Pass the upcoming and past trips to the template
        context = {
            'upcoming_trips': upcoming_trips,
            'past_trips': past_trips,
        }

        if request.method == 'POST':
            trip_id = request.POST.get('trip_id')
            if trip_id:
                # Redirect to the itinerary view with the selected trip's ID
                #return redirect('itinerary', trip_id=trip_id)
                trip = get_object_or_404(Trips, pk=trip_id)
                itinerary = Itinerary.objects.filter(trip=trip)
                location = Location.objects.filter(itinerary__trip=trip)
                
                itin = {
                    'trip': trip,
                    'itinerary': itinerary,
                    'location': location,
                }
                # print(itin)  # Add this line to check the data in the console
                return render(request, 'users/itinerary.html', {'itin': itin})
        else:
            return render(request, 'users/myTrips.html', context)
    else:
        # Handle the case when the user is not logged in (not in session)
        return render(request, 'users/login.html', {'error_message': 'Please log in to view your trips.'})
     

