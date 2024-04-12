
from transformers import pipeline, AutoTokenizer

#Pass in a list of dictionary of articles and display the information in a formatted list


#Function to display the article information
def DisplayArticleInfo(articles):
    #Display Article Info as a formatted list with numbers and content by looping through the list and displaying each dictionary item
    #If the list of articles is empty then display a message
    if len(articles) == 0:
        print("No articles found to display")
    else:
        for i in range(len(articles)):
            print(f"{i+1}. Title: {articles[i]['title']}")
            print(f"    Author: {articles[i]['author']}")
            print(f"    Description: {articles[i]['description']}")
            print(f"    Content: {articles[i]['content']}")
            print(f"    URL: {articles[i]['url']}")
            print(f"    Source: {articles[i]['source']}")
            print(f"    Published Date: {articles[i]['published_date']}")
            print(f"    Image: {articles[i]['image']}")
            print(f"    Sentiment: {articles[i]['sentiment']}")
            print(f"    Keywords: {articles[i]['keywords']}")
            print("\n")
    return None



#Define a function to crete a list of dictionaries of articles
def CreateArticleList(top_headlines):
    #Get News Articles
    articles = top_headlines['articles']

    #Get Article Titles
    titles = [article['title'] for article in articles]

    #Get Article Descriptions
    descriptions = [article['description'] for article in articles]

    #Get Article URLs
    urls = [article['url'] for article in articles]

    #Get Article Content
    content = [article['content'] for article in articles]

    #Get Article Sources
    sources = [article['source']['name'] for article in articles]

    #Get Article Published Dates
    published_dates = [article['publishedAt'] for article in articles]

    #Get Article Authors
    authors = [article['author'] for article in articles]

    #Get Article Images
    images = [article['urlToImage'] for article in articles]

    #Get Article Sentiments
    nlp = pipeline('sentiment-analysis')
    sentiments = [nlp(article['title'])[0] for article in articles]


    #Get Article Keywords
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    keywords = [tokenizer.tokenize(article['title']) for article in articles]

    #Combine Article Info into a dictionary
    for i in range(len(articles)):
        articles[i] = {
            'title': titles[i],
            'author': authors[i],
            'description': descriptions[i],
            'content': content[i],
            'url': urls[i],
            'source': sources[i],
            'published_date': published_dates[i],
            'sentiment': sentiments[i],
            'keywords': keywords[i],
            'image': images[i],
        }

    return articles
    
