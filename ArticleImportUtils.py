#Create a fumction to pull article data from the web
import requests
import os
import sys

from transformers import pipeline, AutoTokenizer
from langdetect import detect
from dotenv import load_dotenv
from newsapi import NewsApiClient

#Create the function to pull the article data passing in country and language
def get_top_headlines(country = None, language = None, query = None):
    
    #Load the API key from the .env file
    load_dotenv()
    news_api_key = os.environ.get('NewsAPIKey2')
    
    #Create the NewsApiClient object
    newsapi = NewsApiClient(news_api_key)
    
    #Get the top headlines from the country and language
    if country == None and language == None:
        top_headlines = newsapi.get_top_headlines(q=query)
    elif country == None:
        top_headlines = newsapi.get_top_headlines(q=query,language=language)
    elif language == None:
        top_headlines = newsapi.get_top_headlines(q=query,country=country)
    else:
        top_headlines = newsapi.get_top_headlines(q=query,country=country, language=language)
    
    #Return the top headlines
    return top_headlines




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
    