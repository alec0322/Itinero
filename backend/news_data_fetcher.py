import requests
import datetime

class NewsAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2/'

    def get_article_titles(self, city):   

        #Calculate the date from a month ago
        current_date = datetime.date.today()
        one_month_ago = current_date - datetime.timedelta(days=30)
        one_month_ago = one_month_ago.strftime("%Y-%m-%d") #Change it to YYYY-MM-DD format

        #Obtain the most relevant articles over the last month related to the inputted 'city'
        url = (
            f'{self.base_url}everything?'
            f'q=+{city}&'
            f'from={one_month_ago}&'
            'language=en&'
            'sortBy=relevancy&'
            f'apiKey={self.api_key}'
        )

        response = requests.get(url)
        data = response.json()

        #Create list to hold the first <= 100 article titles
        article_titles = []

        for article in data["articles"][:100]:
            article_titles.append(article["title"])

        return article_titles
