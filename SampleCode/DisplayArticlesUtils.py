#Pass in a list of dictionary of articles and display the information in a formatted list


#Function to display the article information
def DisplayArticleInfo(articles):
 #   #Display Article Info as a formatted list with numbers and content by looping through the list and displaying each dictionary item
    print(articles)
 #   for i in range(len(articles)):
 #       print(f"{i+1}. Title: {articles[i]['title']}")
 #       print(f"    Description: {articles[i]['description']}")
 #       print(f"    URL: {articles[i]['content']}")
 #       print(f"    URL: {articles[i]['url']}")
 #       print(f"    Source: {articles[i]['source']}")
 #       print(f"    Published Date: {articles[i]['published_date']}")
 #       print(f"    Author: {articles[i]['author']}")
 #       print(f"    Image: {articles[i]['image']}")
 #       print(f"    Sentiment: {articles[i]['sentiment']}")
 #       print(f"    URL: {articles[i]['keywords']}")
 #       print("\n")
    
#'content', 'sentiments', 'keywords', 'descriptions', 'urls', 'sources', 'published_dates', 'authors', and 'images'

# [{'title': titles[i], 'description': descriptions[i], 'url': urls[i], 'content': content[i], 'source': sources[i], 'published_date': published_dates[i], 'author': authors[i], 'image': images[i], 'sentiment': sentiments[i]} for i in range(len(titles))]