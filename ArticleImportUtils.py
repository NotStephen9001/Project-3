#Create a fumction to pull article data from the web
import requests
import os
import sys

from transformers import pipeline, AutoTokenizer
from langdetect import detect
from dotenv import load_dotenv
#from newsapi import NewsApiClient

def get_article_data(country = None, language = None, query = None):
    load_dotenv()

    if query == None or query == "None" or query == "":
        query = "News"
    
    print("Getting article data for query: " + query)

    wrld_news_api_key = os.environ.get('WrldNewsAPIKey')

    url = "https://api.worldnewsapi.com/search-news"

    params = {}

    # Add parameters only if they are provided and not None
    if query:
        params['text'] = query
    if country and country != '':
        params['source-countries'] = country
    if language and language != '':
        params['language'] = language

    print(params)

    headers = {
        'x-api-key': wrld_news_api_key
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    print(get_article_data())





# #Create the function to pull the article data passing in country and language
# def get_top_headlines(country = None, language = None, query = None):
    
#     #Load the API key from the .env file
#     load_dotenv()
#     news_api_key = os.environ.get('NewsAPIKey2')
#     wrld_news_api_key = os.environ.get('WrldNewsAPIKey')
    
#     #Create the NewsApiClient object
#     newsapi = NewsApiClient(news_api_key)
    
#     #Get the top headlines from the country and language
#     if country == None and language == None:
#         top_headlines = newsapi.get_top_headlines(q=query)
#     elif country == None:
#         top_headlines = newsapi.get_top_headlines(q=query,language=language)
#     elif language == None:
#         top_headlines = newsapi.get_top_headlines(q=query,country=country)
#     else:
#         top_headlines = newsapi.get_top_headlines(q=query,country=country, language=language)
    
#     #Return the top headlines
#     return top_headlines




#Define a function to create a list of the number of articles for each country and language combination
def getNumberOfArticles(validCountryCodes, validLanguageCodes):
    #Create a dictionary to hold the number of articles for each country and language combination

    numArticles = {}
    
    #Get the number of articles for each country and language combination
    for country in validCountryCodes:
        if country!= "None":
            print("Getting number of articles for country: " + country)
            for language in validLanguageCodes:
                if language != "None":
                    print("Getting number of articles for language: " + language)
                    top_headlines = get_top_headlines(country, language)
                    numArticles[(country, language)] = len(top_headlines['articles'])
                else:
                    print("Skipping 'None' language code")
        else:
            print("Skipping 'None' country code")
    
        
    
    #Return the dictionary of the number of articles for each country and language combination
    return numArticles
    