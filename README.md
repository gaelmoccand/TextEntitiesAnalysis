# Text Entity Analysis

Using Google Natural Language AI. 
This tool will retrieve entities from a text.
It gives the sentiment analysis score on each entity and on the whole text.
Additionally, it also provides the corresponding categories for the text.
A xls file is generated to store all results.
references:
- https://cloud.google.com/sdk/docs/install
- https://cloud.google.com/natural-language/docs/quickstart-client-libraries
- https://cloud.google.com/natural-language/docs/analyzing-entities
- https://cloud.google.com/natural-language/docs/categories

# 1 Setup

## 1.1 Create virtual environment

```shell
$ python3 -m venv env
$ source env/bin/activate

```

## 1.2 Install packages and Google API key

```shell
$ python3 -m pip install -r requirements.txt

```

## 1.3 cloud sdk

```shell
$ gcloud init (if not run automatically then select your project)
$ gcloud services enable language.googleapis.com
$ gcloud auth application-default login

```


# 2 Usage

```shell
$ python3 getEntity.py --lang en inputTextFile resultsXlsFile

```
