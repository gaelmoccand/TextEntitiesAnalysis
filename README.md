# Text Entity Analysis

Using Google Natural Language AI. This tool will retrieve entities from a text File and provide also a sentiment analasisys for thesee entitites.
It gives also the sentiement score forf the whole text and list also the correspoing categories for the text.
A xlsx file is genereated to store all results

https://cloud.google.com/natural-language/docs/quickstart-client-libraries

# 1 Setup

## 1.1 Create virutal environment

```shell
$ python3 -m venv env
$ source env/bin/activate

```
## 1.2 Install packages and Google API key

```shell
$ python3 -m pip install -r requirements.txt
$ export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"

```

# 2 Usage

```shell
$ python3 getEntity.py --lang en inputFile.txt resultFile 

```
