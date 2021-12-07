# Imports the Google Cloud client library
from pandas.core.indexes.base import ensure_index
from google.cloud import language_v1
import sys
import os
import pandas as pd
import argparse
from gCloudNlp import gNlpApi

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Analyze Entities and Sentiment from text input file ')
    parser.add_argument('InputFile', metavar='path', type=str, help='input text file')
    parser.add_argument('Results', metavar='path', type=str, help='output result .xlsx file')
    parser.add_argument('--lang', default='en', const='en', nargs='?', choices=['en', 'fr', 'de', 'it'],  help='optional specify language [en|fr|de|it]')


    args = parser.parse_args()

    input_path = args.InputFile
    results_path = args.Results
    input_lang = args.lang



    if not os.path.isfile(input_path):
        print('The input text file specified does not exist')
        sys.exit()


    with open(input_path) as file:
        in_text = file.read()
        print(in_text)

        g_nlp = gNlpApi(in_text, input_lang)

        if (input_lang == 'en'):
            df_category = g_nlp.classify_text()
            df_entity = g_nlp.analyze_entity_sentiment()
            df_txt_senti = g_nlp.analyze_text_sentiment()
        else:
            df_category = None
            df_entity = g_nlp.analyze_entity()
            df_txt_senti = g_nlp.analyze_text_sentiment()

        with pd.ExcelWriter(results_path + '.xlsx') as writer:
            df_entity.to_excel(writer, sheet_name='SentimentEntities')
            df_txt_senti.to_excel(writer, sheet_name='SentimentText')
            if df_category is not None:
                df_category.to_excel(writer, sheet_name='Category')

