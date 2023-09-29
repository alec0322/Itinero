import requests
import datetime

class NewsAPI:

    #NewsAPI Constructor
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2/'

    def make_api_request(self, endpoint):
        try:
            url = f'{self.base_url}everything?{endpoint}&apiKey={self.api_key}'
            response = requests.get(url)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None

    #Returns <= 100 articles over the last month related to 'city'
    def get_city_articles(self, city, max_articles=100):   

        #Calculate the date from a month ago
        current_date = datetime.date.today()
        one_month_ago = current_date - datetime.timedelta(days=30)
        one_month_ago = one_month_ago.strftime("%Y-%m-%d") #Change it to YYYY-MM-DD format

        params = (
            f'q=+{city}&'
            f'from={one_month_ago}&'
            'language=en&'
            'sortBy=relevancy'
        )

        data = self.make_api_request(params)

        city_articles = []

        for article in data["articles"][:max_articles]:
            city_articles.append(article["title"])

        return city_articles
    
    #Returns <= 250 crime-related articles over the last month
    def get_crime_articles(self, max_articles=250):

        params = (
            'q=+crime+shooting+killed+dead&'
            'language=en&'
            'sortBy=relevancy'
        )

        data = self.make_api_request(params)

        crime_articles = []

        for article in data["articles"][:max_articles]:
            crime_articles.append(article["title"])

        return crime_articles
    
    #Returns <= 250 non-crime-related articles over the last month
    def get_non_crime_articles(self, max_articles=250):

        params = (
            'q=-crime-shooting-killed-dead&'
            'language=en&'
            'sortBy=relevancy'
        )
        
        data = self.make_api_request(params)

        non_crime_articles = []

        for article in data["articles"][:max_articles]:
            non_crime_articles.append(article["title"])

        return non_crime_articles