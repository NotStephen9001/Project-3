#Create a fumction to pull article data from the web
import requests
import os
import sys

from transformers import pipeline, AutoTokenizer
from dotenv import load_dotenv
from newsapi import NewsApiClient

#Create the function to pull the article data passing in country and language
def get_top_headlines(country = None, language = None):
    
    #Load the API key from the .env file
    load_dotenv()
    news_api_key = os.environ.get('NewsAPIKey')
    
    #Create the NewsApiClient object
    newsapi = NewsApiClient(news_api_key)
    
    #Get the top headlines from the country and language
    if country == None and language == None:
        top_headlines = newsapi.get_top_headlines()
    elif country == None:
        top_headlines = newsapi.get_top_headlines(language=language)
    elif language == None:
        top_headlines = newsapi.get_top_headlines(country=country)
    else:
        top_headlines = newsapi.get_top_headlines(country=country, language=language)
    
    #Return the top headlines
    return top_headlines