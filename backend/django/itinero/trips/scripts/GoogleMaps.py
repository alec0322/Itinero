from unittest import result
from urllib import response
import googlemaps
import requests
import sys
import json
from .API_KEYS import GOOGLE_API_KEY

map_client = googlemaps.Client(API_KEY)




def getCordsFromAddress(input):
    lat, lng = None, None
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={input}&key={API_KEY}"

    req = requests.get(endpoint)
    if req.status_code not in range(200, 299):
        return None, None
    try:
        results = req.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except Exception as e:
        print(f"An error occurred while getting coordinates from address: {e}")
    return lat, lng


# getNearbyPlaces('33028', 'ramen', 'Resturant', 10000)
def getNearbyPlaces(inputlocation, searchForFilter, searchForType, distanceInMeters):
    location = getCordsFromAddress(inputlocation)
    searchFilter = searchForFilter
    distanceInMeters = distanceInMeters

    response = map_client.places_nearby( # type: ignore
        location = location,
        keyword = searchFilter,
        type = searchForType,
        radius = distanceInMeters
    )
    buisnessList = response.get('results')
    # Extract necessary information for each place
    places = [{'name': place['name'], 'address': place['vicinity'], 'place_id': place['place_id']} for place in buisnessList]
    return places

def getPlaceReviews(placeID):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json?"
    endpoint = f"{base_url}place_id={placeID}&key={API_KEY}"

    response = requests.get(endpoint)
    reviewList = response.json()['result']

    if "reviews" in reviewList:
        # Extract necessary information for each review
        reviews = [{'text': review['text'], 'rating': review['rating']} for review in reviewList['reviews']]
        return reviews
    return "None"

#Use this one with an actual location
def getLocationMap(location):
    base_url = "https://maps.googleapis.com/maps/embed/v1/view"
    cords = getCordsFromAddress(location)

    if cords is None:
        print("Unable to get coordinates from address.")
        return None

    endpoint = f"{base_url}?key={API_KEY}&center={str(cords[0])}, {str(cords[1])}"
    response = requests.get(endpoint)

    if response.status_code not in range(200, 299):
        print("Unable to get location map.")
        return None

    return response

def getPlacenMap(location):
    base_url = "https://maps.googleapis.com/maps/embed/v1/view"
    cords = getCordsFromAddress(location)

    if cords is None:
        print("Unable to get coordinates from address.")
        return None

    endpoint = f"{base_url}?key={API_KEY}&q={location}"
    response = requests.get(endpoint)

    if response.status_code not in range(200, 299):
        print("Unable to get place map.")
        return None

    return response
