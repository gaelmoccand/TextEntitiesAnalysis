"""Example of Python client calling Knowledge Graph Search API."""
import json
import sys
import urllib
from urllib.request import Request, urlopen



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
            print("use python knowGraphSearch.py  \"your input\" ")
            self.failed = True
            exit


if __name__ == '__main__':

    arg = ArgParser()
    if not arg.failed:
        api_key = open('.api_key').read()
        #api_key = "zaSyBF7-v2wncy98ARIZNM7_CGrTwUfCiVs4c"
        print(api_key)
        query = arg.input_txt
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        params = {
            'query': query,
            'key': api_key,
            'limit': 6,
            'indent': True,
        }
        url = service_url + '?' + urllib.parse.urlencode(params)
        q = Request(url)
        r = urlopen(q).read()
        response = json.loads(r)
        for element in response['itemListElement']:
            print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')
            print(element['result'].get('description',""))
            print(element['result']['@type'])
            print(element['result'].get('detailedDescription',""))
            print('\n')
