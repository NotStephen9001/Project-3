### Playing with a few diferent summarization models for the time being, nothing here is set in stone

# Function to summarize text
def summarize_text(text, model="facebook/bart-large-cnn"):
    summarization_pipeline = pipeline('summarization', model=model)
    summary = summarization_pipeline(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    return summary

from transformers import pipeline

# Function to translate text to English
def translate_to_english(text, model="Helsinki-NLP/opus-mt-{src_lang}-en"):
    # Dynamically load the translation model based on the detected language
    translation_pipeline = pipeline('translation', model=model.format(src_lang="detected_language"))
    translated_text = translation_pipeline(text)[0]['translation_text']
    return translated_text

for article in articles:
    # Assume you have a function to detect the language
    if detect_language(article['content']) != 'English':
        article['translated_content'] = translate_to_english(article['content'])
    else:
        article['translated_content'] = article['content']
    
    # Summarize the (translated) content
    article['summary'] = summarize_text(article['translated_content'])
