import os
import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient
from transformers import pipeline, AutoTokenizer, MBart50TokenizerFast, MBartForConditionalGeneration

# Load the API key from the .env file and initialize NewsApiClient
load_dotenv()
news_api_key = os.getenv('NewsAPIKey2')
newsapi = NewsApiClient(api_key=news_api_key)

# Sentiment analysis and summarization pipelines
sentiment_analyzer = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

def get_top_headlines(query=None, country=None, language=None):
    """ Fetches top headlines based on query, country, and language. """
    if country is None and language is None:
        return newsapi.get_top_headlines(q=query)
    elif country is None:
        return newsapi.get_top_headlines(q=query, language=language)
    elif language is None:
        return newsapi.get_top_headlines(q=query, country=country)
    else:
        return newsapi.get_top_headlines(q=query, country=country, language=language)

def process_articles(top_headlines):
    """ Process articles by fetching details, analyzing sentiment, and summarizing content. """
    articles = top_headlines['articles']
    for article in articles:
        # Perform sentiment analysis
        article['sentiment'] = sentiment_analyzer(article['content'])[0] if article['content'] else {'label': 'Neutral', 'score': 0}
        # Generate summary
        article['summary'] = summarizer(article['content'], max_length=130, min_length=30, do_sample=False)[0]['summary_text'] if article['content'] else "No summary available."
    return articles

def display_articles(articles):
    """ Displays formatted information for each article, including sentiment and summary. """
    if len(articles) == 0:
        print("No articles found to display.")
    else:
        for i, article in enumerate(articles, start=1):
            print(f"{i}. Title: {article['title']}")
            print(f"   Author: {article['author']}")
            print(f"   Summary: {article['summary']}")
            print(f"   Sentiment: {article['sentiment']['label']} ({article['sentiment']['score']:.2f})")
            print(f"   Content: {article['content']}")
            print(f"   URL: {article['url']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   Published Date: {article['publishedAt']}")
            print(f"   Image: {article['urlToImage']}")
            print("\n")

def main():
    """ Main function to handle the workflow. """
    countryCode = input("Enter the country code for article search: ").lower()
    languageCode = input("Enter the language code for article search: ").lower()
    searchTerm = input("Enter the search term: ").lower()

    top_headlines = get_top_headlines(query=searchTerm, country=countryCode, language=languageCode)
    articles = process_articles(top_headlines)
    display_articles(articles)

if __name__ == "__main__":
    main()
