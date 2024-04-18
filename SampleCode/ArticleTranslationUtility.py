from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM, MBartForConditionalGeneration, MBart50TokenizerFast
from dotenv import load_dotenv
from newsapi import NewsApiClient





def SelectArticleToTranslate(articles):
    #Select the number of the article to translate
    #Make sure the user enters a valid number
    #and is also an integer
    articleNumber = "0"
    while int(articleNumber) < 1 or int(articleNumber) > len(articles):
            articleNumber = input("Please enter the number of the article you would like to translate: ")
            while not articleNumber.isdigit():
                articleNumber = input("Please enter a valid number: ")
    
    articleNumber = int(articleNumber)

    return articleNumber





def TranslateArticle(articles, languageCode, articleNumber):

    print("Translating Article...")

    #Translate the article to English if it is not already in English
    
    article = articles[articleNumber - 1]
    model_name = "facebook/mbart-large-50-many-to-many-mmt"

    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    tokenizer.src_lang = languageCode + "_" + languageCode.upper()

    if languageCode != "en":
        print("Translating article to English...")

        model = MBartForConditionalGeneration.from_pretrained(model_name)

        # Translate the article title to English
        translated_title = TranslateArticleText(article['title'], languageCode, tokenizer, model)


        # Translate the article content to English
        translated_content = TranslateArticleText(article['content'], languageCode, tokenizer, model)
        

        #Display the translated article title and content along with original text
        #print("Translated Title: " + translated_title + "\n")
        #print("Original Title: " + article['title'] + "\n")
        #print("\n")
        #print("Translated Content: " + translated_content + "\n")
        #print("Original Content: " + article['content'] + "\n" + "\n")

        #Assign the translated title and content to the article
        article['title'] = translated_title
        article['content'] = translated_content

        #Insert the translated article back into a new list of articles
        translated_article = []
        translated_article.append(article)

    else:
        print("Article is already in English")
    

    
    #Return the translated article as a dictionary
    return translated_article


def TranslateArticleText(inputText, languageCode, tokenizer, model):
     
    #If input text is None change it to an empty string
    if inputText != None:
      # Translate the article part to English
        input_text = inputText
        encoded_text = tokenizer(input_text, return_tensors="pt")

        output_ids = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])

        # Retrieve the text from the special characters.
        translated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    else:
        translated_text = ""
     
    return translated_text
