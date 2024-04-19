import os
import datetime
import logging
import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient
from transformers import pipeline
import spacy
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# Load environment variables and initialize services
load_dotenv()
news_api_key = os.getenv('NEWS_API_KEY', 'your_default_api_key_here')
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
newsapi = NewsApiClient(api_key=news_api_key)
nlp = spacy.load("en_core_web_sm")
tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

# Initialize pipelines with configurable model names
sentiment_model = os.getenv('SENTIMENT_MODEL', 'nlptown/bert-base-multilingual-uncased-sentiment')
summarization_model = os.getenv('SUMMARIZATION_MODEL', 'facebook/bart-large-cnn')
sentiment_analyzer = pipeline('sentiment-analysis', model=sentiment_model)
summarizer = pipeline('summarization', model=summarization_model)

def get_top_headlines(query=None, country=None, language=None):
    # Fetch top headlines based on provided criteria.
    try:
        date_today = datetime.datetime.now()
        date_two_days_ago = date_today - datetime.timedelta(days=2)
        return newsapi.get_everything(q=query, from_param=date_two_days_ago.strftime('%Y-%m-%d'),
                                      to=date_today.strftime('%Y-%m-%d'), language=language, sort_by='relevancy')
    except Exception as e:
        logging.error("Failed to fetch top headlines: %s", str(e))
        return []

def preprocess_text(articles):
    # Preprocess article content
    texts = []
    for article in articles:
        if article['content']:
            raw = article['content'].lower()
            tokens = tokenizer.tokenize(raw)
            stopped_tokens = [i for i in tokens if not i in stop_words]
            texts.append(stopped_tokens)
    return texts

def perform_lda(texts):
    # Perform LDA to identify main topics in the articles.
    try:
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        num_topics = int(os.getenv('LDA_TOPICS', 5))
        lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
        topics = lda_model.print_topics(num_words=3)
        return topics
    except Exception as e:
        logging.error("Failed to perform LDA: %s", str(e))
        return []

def extract_entities(articles):
    # Extract key entities from articles using NER.
    entities = []
    for article in articles:
        if article['content']:
            doc = nlp(article['content'])
            entities.extend([(X.text, X.label_) for X in doc.ents])
    return entities

def display_articles(articles):
    # Displays articles including sentiment and summaries.
    for i, article in enumerate(articles, start=1):
        summary = "No summary available."
        sentiment = {'label': 'Neutral', 'score': 0}
        if article['content']:
            try:
                summary = summarizer(article['content'], max_length=250, min_length=50, do_sample=False)[0]['summary_text']
                sentiment = sentiment_analyzer(article['content'])[0]
            except Exception as e:
                logging.error("Error in processing article %d: %s", i, str(e))
        print(f"{i}. Title: {article['title']}")
        print(f"   Author: {article['author']}")
        print(f"   Summary: {summary}")
        print(f"   Sentiment: {sentiment['label']} ({sentiment['score']:.2f})")
        print(f"   Content: {article['content']}")
        print(f"   URL: {article['url']}")
        print(f"   Source: {article['source']['name']}")
        print(f"   Published Date: {article['publishedAt']}")
        print(f"   Image: {article['urlToImage']}")
        print("\n")

def main():
    # Main Function
    try:
        while True:
            print("1. Search Articles\n2. Exit")
            choice = input("Choose an option: ")
            if choice == '2':
                break
            country_code = input("Enter the country code for article search: ").lower()
            language_code = input("Enter the language code for article search: ").lower()
            search_term = input("Enter the search term: ").lower()

            articles = get_top_headlines(query=search_term, country=country_code, language=language_code)
            if articles:
                display_articles(articles)
                texts = preprocess_text(articles)
                topics = perform_lda(texts)
                entities = extract_entities(articles)

                print("Identified Topics:")
                for topic in topics:
                    print(topic)

                print("\nKey Entities Found:")
                for entity in set(entities):
                    print(entity)
            else:
                print("No articles found.")
    except KeyboardInterrupt:
        print("Exiting program.")

if __name__ == "__main__":
    main()
