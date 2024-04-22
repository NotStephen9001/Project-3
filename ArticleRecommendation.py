import gradio as gr
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
        
        if 'news' in response_data and response_data['news']:
            return response_data['news']
        else:
            return []
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
    recommended_indices = np.argsort(similarities)[::-1][1:]
    return recommended_indices

# Main function to get recommendations
def get_article_recommendations(query):
    articles = fetch_articles_from_api(query)
    
    if not articles:
        return "No articles found for the given query."
    
    article_texts = [article['text'] for article in articles if 'text' in article]
    
    if not article_texts:
        return "No content available in the fetched articles."
    
    embeddings = get_spacy_embeddings(article_texts)
    
    if not embeddings:
        return "Could not generate embeddings from the articles."
    
    try:
        current_article_index = 0
        recommended_indices = recommend_articles(embeddings[current_article_index], embeddings)
        # Return recommended article titles
        return '\n'.join([articles[index]['title'] for index in recommended_indices])
    except IndexError as e:
        return f"Index error: {e}"

# Gradio UI Elements
text_keyword = gr.Textbox(
    label="Search Term",
    placeholder="Enter your search term here"
)

text_results = gr.TextArea(label="Results")

# Gradio App Interface
app = gr.Interface(
    fn=get_article_recommendations,  # Hook up the article recommendation function
    inputs=text_keyword,            # Assuming you only need the keyword for now
    outputs=text_results            # Output the results in a TextArea
)

app.launch(show_error=True)