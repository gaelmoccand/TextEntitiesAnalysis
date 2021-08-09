# Text Entity Analysis

Using Google Natural Language AI. 
This tool will retrieve entities from a text.
It gives the sentiment analysis score on each entity and on the whole text.
Additionally, it also provide the corresponding categories for the text.
An xls file is genereated to store all results.

https://cloud.google.com/natural-language/docs/quickstart-client-libraries

# 1 Setup

## 1.1 Create virtual environment

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
$ python3 getEntity.py --lang en inputTextFile resultsXlsFile

```
