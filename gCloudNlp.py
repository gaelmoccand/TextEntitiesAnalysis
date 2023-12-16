# Imports the Google Cloud client library
from pandas.core.indexes.base import ensure_index
from google.cloud import language_v2, language_v1
import sys
import pandas as pd



class gNlpApi:
    """
    Class to wrap google Natural Language API

    Args:
        text : the input text read from file to be analyzed. Must include at least 20 char.
        lang : language english is default [en, de, fr, it]
    """



    def __init__(self, text, lang):
        if len(text) < 20:
            print("Text is too short. It must be at least 20 characters")
            sys.exit()
        else:
            self.input_txt = text
            self.input_lang = lang
            self.client = language_v2.LanguageServiceClient()
            self.client_v1 = language_v1.LanguageServiceClient()





    def analyze_entity_sentiment(self):
        """
        Analyzing Entity Sentiment in a String or Text

        Args:

        Return:
            df : Panda Data Frame with the entities analysis

        """

        res = {
            'Name': [],
            'Type': [],
            'Salience': [],
            'Score': [],
            'Magnitude': [],
            'Metadatas': [],
            'Mentions': [],
        }

        type_ = language_v1.Document.Type.PLAIN_TEXT

        document = {"content": self.input_txt, "type_": type_, "language": self.input_lang}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = language_v1.EncodingType.UTF32

        response = self.client_v1.analyze_entity_sentiment(
            request={'document': document, 'encoding_type': encoding_type})

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
            metadatas = str()
            for metadata_name, metadata_value in entity.metadata.items():
                print(u"{} = {}".format(metadata_name, metadata_value))
                metadatas += u" {} = {}; ".format(metadata_name, metadata_value)

            res['Metadatas'].append(metadatas)


            # Loop over the mentions of this entity in the input document.
            # The API currently supports proper noun mentions.
            mentions = str()
            for mention in entity.mentions:
                print(u"Mention text: {}".format(mention.text.content))
                # Get the mention type, e.g. PROPER for proper noun
                print(u"Mention type: {}".format(language_v2.EntityMention.Type(mention.type_).name))
                mentions += "{} : {}; ".format(mention.text.content, language_v2.EntityMention.Type(mention.type_).name)
            res['Mentions'].append(mentions)


            print(u"\n")

        # Get the language of the text, which will be the same as
        # the language specified in the request or, if not specified,
        # the automatically-detected language.
        print(u"Language of the text: {}".format(response.language))
        df = pd.DataFrame(res)
        return df


    def analyze_entity(self):
        """
        Analyzing Entity in a String or Text

        Args:

        Return:
            df : Panda Data Frame with the entities analysis

        """

        res = {
            'Name': [],
            'Type': [],
            'Salience': [],
            'Metadatas': [],
        }

        type_ = language_v1.Document.Type.PLAIN_TEXT

        document = {"content": self.input_txt, "type_": type_, "language": self.input_lang}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = language_v1.EncodingType.UTF32

        response = self.client_v1.analyze_entities(
            request={'document': document, 'encoding_type': encoding_type})

        print(u" Entities:\n")
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

            # Loop over the metadata associated with entity. For many known entities,
            # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
            # Some entity types may have additional metadata, e.g. ADDRESS entities
            # may have metadata for the address street_name, postal_code, et al.
            metadatas = str()
            for metadata_name, metadata_value in entity.metadata.items():
                print(u"{} = {}".format(metadata_name, metadata_value))
                metadatas += u" {} = {}; ".format(metadata_name, metadata_value)

            res['Metadatas'].append(metadatas)

        # Get the language of the text, which will be the same as
        # the language specified in the request or, if not specified,
        # the automatically-detected language.
        print(u"Language of the text: {}".format(response.language))
        df = pd.DataFrame(res)
        return df



    def classify_text(self):
        """
        Classifying Content in a String

        Args:
            none
        Return:
            df : Panda Data Frame with the entities analysis
        """


        type_ = language_v1.Document.Type.PLAIN_TEXT

        document = {"content": self.input_txt, "type_": type_, "language": self.input_lang}

        res = {
            'Name': [],
            'Confindence': [],
        }

        content_categories_version = (
            language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
        )
        response = self.client_v1.classify_text(
            request={
                "document": document,
                "classification_model_options": {
                    "v2_model": {"content_categories_version": content_categories_version}
                },
            }
        )
        # Loop through classified categories returned from the API
        for category in response.categories:
            # Get the name of the category representing the document.
            # See the predefined taxonomy of categories:
            # https://cloud.google.com/natural-language/docs/categories
            print(u"Category name: {} confidence {}".format(category.name, category.confidence))
            # Get the confidence. Number representing how certain the classifier
            # is that this category represents the provided text.
            res['Name'].append((category.name))
            res['Confindence'].append((category.confidence))

        df = pd.DataFrame(res)
        return df


    def analyze_text_sentiment(self):
        document = language_v2.Document(
            content=self.input_txt, type_=language_v2.Document.Type.PLAIN_TEXT)

        res = {
            'Score': [],
            'Magnitude': [],
        }

        # Detects the sentiment of the text
        sentiment = self.client.analyze_sentiment(request={'document': document}).document_sentiment
        print("whole Text Sentiment: {}, magnitude: {}".format(sentiment.score, sentiment.magnitude))

        res['Score'].append((sentiment.score))
        res['Magnitude'].append((sentiment.magnitude))
        df = pd.DataFrame(res)
        return df

