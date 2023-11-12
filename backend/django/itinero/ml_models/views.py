from django.shortcuts import render
from django.http import JsonResponse
# from .itinero_model import CrimeClassifier
# from .place_recommender import recommendPlace

# def recommend_view(request):
#     # Get the parameters from the request
#     location = request.GET.get('location')
#     sentence = request.GET.get('sentence')
#     distance = request.GET.get('distance')

#     # Recommend a place
#     best_place = recommendPlace(location, sentence, distance)

#     # Return the result as a JSON response
#     return JsonResponse({'best_place': best_place})
