from django.http import JsonResponse
from django.db.models import F, Value, functions
from django.db.models.functions import Concat
from django.shortcuts import render, redirect, get_object_or_404
from .models import City, State, Itinerary, Location, Trips
# from .itinero_model import CrimeClassifier
from .scripts.place_recommender import recommendPlace


def recommend_view(request):
    # Get the parameters from the request
    location = request.GET.get('location')
    sentence = request.GET.get('sentence')
    distance = request.GET.get('distance')

    # Recommend a place
    best_place = recommendPlace(location, sentence, distance)

    # Return the result as a JSON response
    return JsonResponse({'best_place': best_place})


def search_locations(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'Missing query parameter'}, status=400)
    
    city_results = City.objects.filter(name__icontains=query).annotate(
        full_name=Concat('name', Value(', '), 'state__name')
    )
    state_results = State.objects.filter(name__icontains=query).annotate(
        full_name=F('name')
    )
    data = {
        'locations': list(city_results.values('full_name')) + list(state_results.values('full_name')),
    }
    return JsonResponse(data, safe=False)

def create_itinerary(request):
    if request.method == 'POST':
        # Get the form data
        trip_id = request.POST['trip_id']
        date = request.POST['date']
        hotel = request.POST['hotel']

        # Get the trip
        trip = get_object_or_404(Trips, id=trip_id)

        # Create the itinerary
        itinerary = Itinerary.objects.create(trip=trip, date=date, hotel=hotel)

        # Generate the places for each time slot
        for time_slot in Location.TIME_SLOT_CHOICES:
            # Call your function to generate the places here
            places = recommendPlace(location="Location", sentence=time_slot[0], distance="Distance")

            # Create the location
            Location.objects.create(
                itinerary=itinerary,
                time_slot=time_slot[0],
                name="Location name",  # Replace with actual name
                time="Time",  # Replace with actual time
                activity="Activity",  # Replace with actual activity
                search_keyword="Keyword",  # Replace with actual keyword
                place="Place",  # Replace with actual place
                places=places
            )

        return redirect('itinerary', itinerary_id=itinerary.id)

    else:
        # Render the form
        return render(request, 'create_itinerary.html')