from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import GoogleMaps
import itertools

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def recommendPlace(location, sentence, distance):
    embeddings1 = model.encode(sentence)
    placesSearched = GoogleMaps.getNearbyPlaces(location, sentence, "", distance)
    scoredPlaces = []

    for i, place in enumerate(placesSearched):
        reviews = GoogleMaps.getPlaceReviews(place["place_id"])
        reviewNum = 0
        averageScore = 0
        totalRating = 0
        
        if(reviews != "None"):
            for review in itertools.islice(reviews, 50):
                reviewNum += 1
                reviewEmbeded = model.encode(review["text"])
                averageScore += util.cos_sim(embeddings1, reviewEmbeded) # type: ignore
                totalRating += review['rating']

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
    return scoredPlaces


location = "Miami, Fl"
sentence = ["Hotels"]
distance = 15000

best_place = recommendPlace(location, sentence, distance)

for place in best_place:
    print(f"Name: {place['name']}")
    print(f"Address: {place['address']}")
    print(f"Rating: {place['average_rating']}")
    print(f"Review Score: {format(place['review_score'].item(), '.2f')}\n")