# Imports the Google Cloud client library
from pandas.core.indexes.base import ensure_index
from google.cloud import language_v1
import sys
import pandas as pd



client = language_v1.LanguageServiceClient()


class ArgParser:

    inputTxt = str()
    outputRes = str()
    failed = False
    def __init__(self):
        if len(sys.argv) == 3:
            self.outputRes = str(sys.argv.pop()) 
            self.inputTxt = str(sys.argv.pop())

        else:
            print("Too few arguments")
            print("Syntax:")
            print("use txtanalysis.py  textFileName resultFileName")
            self.failed = True
            exit


def analyze_entity_sentiment(text_content):
    """
    Analyzing Entity Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    res = {
            'Name': [],
            'Type': [],
            'Salience': [],
            'Score': [],
            'Magnitude': [],
          }


    # text_content = 'Grapes are good. Bananas are bad.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    print(u"Sentiment Entities:\n")
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        res['Name'].append(format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        ent = language_v1.Entity.Type(entity.type_).name
        print(u"Entity type: {}".format(ent))
        res['Type'].append(ent)

        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        res['Salience'].append((entity.salience))

        # Get the aggregate sentiment expressed for this entity in the provided document.
        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        res['Score'].append((sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        res['Magnitude'].append((sentiment.magnitude))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
            )

        print(u"\n")

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))
    df = pd.DataFrame(res)
    return df


def classify_text(text_content):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """


    # text_content = 'That actor on TV makes movies in Hollywood and also stars in a variety of popular new TV shows.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    res = {
        'Name': [],
        'Confindence': [],
    }


    response = client.classify_text(request = {'document': document})
    # Loop through classified categories returned from the API
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        print(u"Category name: {} confidence {}".format(category.name,category.confidence ))
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        res['Name'].append((category.name))
        res['Confindence'].append((category.confidence))

    df = pd.DataFrame(res)
    return df

def analyze_text_sentiment(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    res = {
        'Score': [],
        'Magnitude': [],
    }

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    print("whole Text Sentiment: {}, magnitude: {}".format(sentiment.score, sentiment.magnitude))
    res['Score'].append((sentiment.score))
    res['Magnitude'].append((sentiment.magnitude))
    df = pd.DataFrame(res)
    return df


if __name__ == '__main__':


    arg = ArgParser()
    if not arg.failed:

        # The text to analyze
        text = str()

        with open(arg.inputTxt) as f:
            contents = f.read()
            text = contents
            print(contents)

        dfcategory = classify_text(text)

        dfsenti = analyze_entity_sentiment(text)

        dftxtsenti= analyze_text_sentiment(text)

        with pd.ExcelWriter(arg.outputRes +'.xlsx') as writer:  
            dfsenti.to_excel(writer, sheet_name='SentimentEntities')
            dfcategory.to_excel(writer, sheet_name='Category')
            dftxtsenti.to_excel(writer, sheet_name='SentimentText')


