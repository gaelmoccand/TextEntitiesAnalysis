from __future__ import print_function
import json
import urllib
import urllib.parse
from urllib.request import Request, urlopen
import os
import sys
import datetime
from collections import OrderedDict
import time
import shutil
import time
from inspect import getsourcefile
from os.path import abspath



# parsing argument for cmd line arg
class ArgParser:

    input_txt = str()
    failed = False
    def __init__(self):
        if len(sys.argv) == 2:
            self.input_txt = str(sys.argv.pop()) 
        else:
            print("Too few arguments")
            print("Syntax:")
            print("use .py  \"text\" ")
            self.failed = True
            exit


if __name__ == '__main__':

    arg = ArgParser()
    if not arg.failed:
        api_key = os.environ.get('API_KEY')
        print(api_key)
        query = arg.input_txt
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        params = {
            'query': query,
            'key': api_key,
            'limit': 3,
            'indent': True,
        }
        url = service_url + '?' + urllib.parse.urlencode(params)
        q = Request(url)
        r = urlopen(q).read()
        response = json.loads(r)
        for element in response['itemListElement']:
            print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')
            print(element['result']['description'])
            print(element['result']['@type'])
            print(element['result']['detailedDescription'])
            print('\n')
    
