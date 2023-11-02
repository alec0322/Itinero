from urllib import response
import googlemaps
import requests
import sys
import json

API_KEY = 'AIzaSyAwNPEp6NIjh_sIXhUbVnsZq34R28mrjPs'

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
def getNearbyPlaces(inputlocation, searchForType, searchForFilter, distanceInMeters):
    location = getCordsFromAddress(inputlocation)
    print(location)
    searchFilter = searchForFilter
    distanceInMeters = distanceInMeters


    response = map_client.places_nearby(
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

    reviewList = response.json()['result']['reviews']
    return reviewList
    
    # for i, buisness in enumerate(reviewList):
    #     print(reviewList[i]['rating'])
    #     print(reviewList[i]['text'])


def getLocationMap(location):
    base_url = "https://maps.googleapis.com/maps/embed/v1/view"

    cords = getCordsFromAddress(location)

    endpoint = f"{base_url}?key={API_KEY}&center={str(cords[0])}, {str(cords[1])}"

    response = requests.get(endpoint)
    print(response.text)

