from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import GoogleMaps
import itertools


sentence = ["steak"]


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def reccomendPlace(location, sentence, distance):
    embeddings1 = model.encode(sentence)
    highestScore = 0
    bestPlace = ''
    placesSearched = GoogleMaps.getNearbyPlaces("33028", sentence, "", 10000)

    for i, places in enumerate(placesSearched):
        reviews = GoogleMaps.getPlaceReviews(places["place_id"])
        reviewNum = 0
        averageScore = 0
        
        if(reviews != "None"):
            for review in itertools.islice(reviews, 50):
                reviewNum += 1
                reviewEmbeded = model.encode(review["text"])
                
                averageScore += util.cos_sim(embeddings1, reviewEmbeded) # type: ignore

        averageScore /= reviewNum
        if averageScore > highestScore:
            highestScore = averageScore
            bestPlace = places["place_id"]
        
        
    return bestPlace

