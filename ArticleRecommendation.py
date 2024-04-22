import requests
import spacy
import numpy as np

# Load the medium-sized spaCy model with vectors
nlp = spacy.load('en_core_web_md')

# Function to fetch articles from World News API
def fetch_articles_from_api(query, api_key):
    url = "https://api.worldnewsapi.com/search-news"
    headers = {'x-api-key': api_key}
    params = {'text': query}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    else:
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
    # Get indices of articles sorted by similarity (excluding the target article itself)
    recommended_indices = np.argsort(similarities)[::-1][1:]
    return recommended_indices

# Main function to get recommendations
def get_article_recommendations(query, api_key):
    # Fetch articles from the API
    articles = fetch_articles_from_api(query, api_key)
    
    # Extract text content from articles
    article_texts = [article['content'] for article in articles]
    
    # Generate embeddings for each article
    embeddings = get_spacy_embeddings(article_texts)
    
    # Assume the first article is the target for recommendations
    current_article_index = 0
    recommended_indices = recommend_articles(embeddings[current_article_index], embeddings)
    
    # Print recommended articles
    for index in recommended_indices:
        print(articles[index]['title'])

# Use your API key and desired query to get recommendations
your_api_key = 'WrldNewsAPIKey'
query = 'latest news'
get_article_recommendations(query, your_api_key)