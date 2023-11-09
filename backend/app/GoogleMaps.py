from unittest import result
from urllib import response
import googlemaps
import requests
import sys
import json

API_KEY = ''

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
    except:
        pass
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
    return buisnessList

    # for i, buisness in enumerate(buisnessList):
    #     print(buisnessList[i]['name'])
        

def getPlaceReviews(placeID):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json?"
    endpoint = f"{base_url}place_id={placeID}&key={API_KEY}"

    response = requests.get(endpoint)
    reviewList = response.json()['result']

    if "reviews" in reviewList:
        return reviewList['reviews']
    return "None"
    
    # for i, buisness in enumerate(reviewList):
    #     print(reviewList[i]['rating'])
    #     print(reviewList[i]['text'])

#Use this one with an actual location
def getLocationMap(location):
    base_url = "https://maps.googleapis.com/maps/embed/v1/view"

    cords = getCordsFromAddress(location)

    endpoint = f"{base_url}?key={API_KEY}&center={str(cords[0])}, {str(cords[1])}"

    response = requests.get(endpoint)
    return response


##Use this one with a place id
def getPlacenMap(location):
    base_url = "https://maps.googleapis.com/maps/embed/v1/view"

    cords = getCordsFromAddress(location)

    endpoint = f"{base_url}?key={API_KEY}&q={location}"

    response = requests.get(endpoint)
    return response
