import requests
import spacy
import numpy as np
from dotenv import load_dotenv
import os

# Load the medium-sized spaCy model with vectors
nlp = spacy.load('en_core_web_md')

# Load environment variables from the .env file
load_dotenv()

# Function to fetch articles from World News API
def fetch_articles_from_api(query):
    url = "https://api.worldnewsapi.com/search-news"
    api_key = os.getenv('WrldNewsAPIKey')
    headers = {'x-api-key': api_key}
    params = {'text': query}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        response_data = response.json()
        print(response_data.keys())
        
        if 'news' in response_data and response_data['news']:
            # Log the first article to check its structure
            print("First article in response:", response_data['news'][0])
            return response_data['news']
        else:
            print("The 'news' key is empty or not present in the response.")
            return []
    else:
        print(response.text)
        raise Exception(f"World News API Error: {response.status_code}")

# Function to generate embeddings using spaCy
def get_spacy_embeddings(texts):
    embeddings = [nlp(text).vector for text in texts]
    return embeddings

# Function to calculate similarity between two vectors
def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

# Function to recommend articles
def recommend_articles(target_article_embedding, all_article_embeddings):
    similarities = [cosine_similarity(target_article_embedding, embedding) for embedding in all_article_embeddings]
    recommended_indices = np.argsort(similarities)[::-1][1:]
    return recommended_indices

# Main function to get recommendations
def get_article_recommendations(query):
    # Fetch articles from the API using the query
    articles = fetch_articles_from_api(query)
    
    if not articles:
        print("No articles found for the given query.")
        return

    # Extract text content from articles
    article_texts = [article['text'] for article in articles if 'text' in article]
    
    if not article_texts:
        print("No content available in the fetched articles.")
        return

    # Generate embeddings for each article
    embeddings = get_spacy_embeddings(article_texts)
    
    if not embeddings:
        print("Could not generate embeddings from the articles.")
        return
    
    try:
        # Assume the first article is the target for recommendations
        current_article_index = 0
        recommended_indices = recommend_articles(embeddings[current_article_index], embeddings)
        
        # Print recommended articles
        for index in recommended_indices:
            print(articles[index]['title'])
    except IndexError as e:
        print(f"Index error: {e}")

# Use the query to get recommendations
query = 'latest news'
get_article_recommendations(query)