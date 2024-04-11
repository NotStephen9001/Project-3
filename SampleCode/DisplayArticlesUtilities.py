#Pass in a list of dictionary of articles and display the information in a formatted list


#Function to display the article information
def DisplayArticleInfo(articles):
    #Display Article Info as a formatted list with numbers and content by looping through the list and displaying each dictionary item
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
    
