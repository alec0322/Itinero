from sentence_transformers import SentenceTransformer
from sentence_transformers import util
from .GoogleMaps import *
import itertools
import numpy as np
import json

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def recommendPlace(location, sentence, distance):
    embeddings1 = model.encode(sentence)
    placesSearched = getNearbyPlaces(location, sentence, "", distance)
    scoredPlaces = []

    for i, place in itertools.islice(enumerate(placesSearched), 15):
        reviews = getPlaceReviews(place["place_id"])
        reviewNum = 0
        averageScore = 0
        totalRating = 0

        if(reviews != "None"):
            for review in itertools.islice(reviews, 20):
                reviewNum += 1
                reviewEmbeded = model.encode(review["text"])
                averageScore += util.cos_sim(embeddings1, reviewEmbeded) # type: ignore

        averageScore /= reviewNum
        averageRating = totalRating / reviewNum if reviewNum > 0 else 0
        # Normalize the average score to a 1-5 scale
        normalizedScore = 1 + 4 * (averageScore + 1) / 2
        scoredPlace = {
            'name': place['name'],
            'address': place['address'],
            'review_score': normalizedScore,
            'average_rating': averageRating
        }
        scoredPlaces.append(scoredPlace)
        
    scoredPlaces.sort(key=lambda x: x['review_score'], reverse=True)
    
    # Convert Tensor objects to NumPy arrays
    np_scoredPlaces = []
    for place in scoredPlaces:
        np_place = {
            'name': place['name'],
            'address': place['address'],
            'review_score': float(place['review_score']),
            'average_rating': float(place['average_rating'])
        }
        np_scoredPlaces.append(np_place)

    return np_scoredPlaces


# location = "Miami, Fl"
# sentence = ["Hotels"]
# distance = 15000

# best_place = recommendPlace(location, sentence, distance)

# for place in best_place:
#     print(f"Name: {place['name']}")
#     print(f"Address: {place['address']}")
#     print(f"Rating: {place['average_rating']}")
#     print(f"Review Score: {format(place['review_score'].item(), '.2f')}\n")