from news_data_fetcher import NewsAPI
from itinero import CrimeClassifier

#Establish API connection
api_key = "1f2e3aff9ef144a99d66c1dd6bf3a6b7"
news_api = NewsAPI(api_key=api_key)

#Wait for user to specify what city they want to travel to (Pseudocode)
'''
city = input("Which city would you like to travel to?\n")
city_articles = news_api.get_city_articles(city)
'''

#Create labeled dataset for the model
training_data = {}
training_data["crime_articles"] = news_api.get_crime_articles()
training_data["non_crime_articles"] = news_api.get_non_crime_articles()

print(training_data) #Prints the training_data to be given to the model

#Utilize Itinero to classify any crime-related articles (Pseudocode)
'''
crime_classifier = CrimeClassifier()

crime_related_titles = []
for title in city_articles:
    if crime_classifier.classify_articles(title):
        crime_related_titles.append(title)

print(crime_related_titles)
'''
