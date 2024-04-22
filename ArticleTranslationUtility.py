from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM, MBartForConditionalGeneration, MBart50TokenizerFast
from dotenv import load_dotenv
#from newsapi import NewsApiClient
from langdetect import detect





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

    #if LanguageCode is None, detect the language of the article
    #if languageCode == None or languageCode == "" or languageCode == "None":
    languageCode = detect(articles[articleNumber - 1]['content'])
        
    print("Detected Language: " + languageCode)
    

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
        
        #Put the returned article into a list
        translated_article = []
        translated_article.append(article)
   

    
    #Return the translated article as a dictionary
    return translated_article


def TranslateArticleText(inputText, languageCode, tokenizer, model):
     
    #If input text is None change it to an empty string
    if inputText != None:
        # Translate the article part to English
        input_text = inputText
        encoded_text = tokenizer(input_text, return_tensors="pt")

        #Break the inputText into 1024 token chunks and loop through each chunk
        #to translate the entire inputText
        #The reassmble the chunks into the translated text
        #This is necessary because the model has a limit of 1024 tokens
        #for each translation

        #Get the number of chunks
        num_chunks = len(encoded_text.input_ids[0]) // 1024
        if len(encoded_text.input_ids[0]) % 1024 != 0:
            num_chunks += 1

        #Initialize the translated text
        translated_text = ""

        #Loop through each chunk and translate it
        for i in range(num_chunks):
            #Get the start and end token indices for the chunk
            start = i * 1024
            end = (i + 1) * 1024
            if end > len(encoded_text.input_ids[0]):
                end = len(encoded_text.input_ids[0])

            #Get the chunk of text
            chunk = input_text[start:end]

            #Encode the chunk
            encoded_chunk = tokenizer(chunk, return_tensors="pt")

            #Translate the chunk
            output_ids = model.generate(**encoded_chunk, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])

            #Retrieve the text from the special characters.
            translated_chunk = tokenizer.decode(output_ids[0], skip_special_tokens=True)

            #Add the translated chunk to the translated text
            translated_text += translated_chunk
    else:
        translated_text = ""
     
    return translated_text
