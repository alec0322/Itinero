from itinero_model import CrimeClassifier
from news_data_fetcher import NewsAPI

# Establish API connection
news_api = NewsAPI()

# Wait for user to specify what city they want to travel to
city = input("Which city would you like to travel to?\n")
city_articles = news_api.get_city_articles(city)

# Utilize Itinero to classify any crime-related articles
crime_classifier = CrimeClassifier()

# The model returns a set of articles which could potentially be crime-related
print(crime_classifier.classify_articles(city_articles))
