

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
            #print(f"    Description: {articles[i]['description']}")
            print(f"    Content: {articles[i]['content']}")
            print(f"    URL: {articles[i]['url']}")
            #print(f"    Source: {articles[i]['source']}")
            print(f"    Published Date: {articles[i]['published_date']}")
            print(f"    Image: {articles[i]['image']}")
            print(f"    Sentiment: {articles[i]['sentiment']}")
            #print(f"    Keywords: {articles[i]['keywords']}")
            print("\n")
    return None



#Define a function to crete a list of dictionaries of articles
def CreateArticleList(top_headlines):
    #Get News Articles
    articles = top_headlines['news']

    
    #Get Article Titles
    titles = [article['title'] for article in articles]

    #Get Article Descriptions
    #descriptions = [article['description'] for article in articles]

    #Get Article URLs
    urls = [article['url'] for article in articles]

    #Get Article Content
    content = [article['text'] for article in articles]

    #Get Article Sources
    #sources = [article['source']['name'] for article in articles]

    #Get Article Published Dates
    published_dates = [article['publish_date'] for article in articles]

    #Get Article Authors
    authors = [article['authors'] for article in articles]

    #Get Article Images
    images = [article['image'] for article in articles]

    #Get Article Sentiments
    nlp = pipeline('sentiment-analysis')
    sentiments = [nlp(article['title'])[0] for article in articles]


    #Get Article Keywords
    # tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    # keywords = [tokenizer.tokenize(article['text']) for article in articles]

    #Combine Article Info into a dictionary
    for i in range(len(articles)):
        articles[i] = {
            'title': titles[i],
            'author': authors[i],
            #'description': descriptions[i],
            'content': content[i],
            'url': urls[i],
            #'source': sources[i],
            'published_date': published_dates[i],
            'sentiment': sentiments[i],
            #'keywords': keywords[i],
            'image': images[i],
        }

    return articles


def DisplayTranslatedArticle(translated_article):
    #Display the translated article title and content
    print("Translated Article:" + "\n\n")
    print(f"Translated Title: {translated_article[0]['title']}\n")
    print(f"  Author: {translated_article[0]['author']}\n")
    #print(f"  Description: {translated_article[0]['description']}\n")
    print(f"  Content: {translated_article[0]['content']}\n")
    print(f"  URL: {translated_article[0]['url']}\n")
    #print(f"  Source: {translated_article[0]['source']}\n")
    print(f"  Published Date: {translated_article[0]['published_date']}\n")
    print(f"  Image: {translated_article[0]['image']}\n")
    print(f"  Sentiment: {translated_article[0]['sentiment']}\n")
    #print(f"  Keywords: {translated_article[0]['keywords']}\n")
    print("\n")

    
    return None
    
