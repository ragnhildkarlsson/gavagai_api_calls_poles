import json
import requests
from requests.auth import HTTPBasicAuth
POLES_KEY = 'poles'
ID_KEY = 'id'
NAME_KEY = "name"
TERM_KEY = "term"
DESCRIPTION_KEY = "description"
LANGUAGE_KEY = "language"
PARTS_KEY = "parts"
WEIGHT_KEY = "weight"

BASE_URL = 'https://ethersource.gavagai.se/ethersource/rest/v2/poles'
END_URL = '?'
AUTH = 'apiKey=123'
#/1037/suggest?apiKey=123

TEST_CATEGORIES_FILE = 'test_categories.txt'

def get_categories(filepath):
    categories = []
    with open(filepath) as f:
        categories = f.readlines()
        categories = [category.rstrip() for category in categories]
    return categories

def get_body_create_pool(category, name_key, description_key, language_key, part_key, term_key, weight_key):
    data = {}
    data[name_key] = category
    data[description_key] = "vide text categorization"
    data[language_key] = "EN"
    parts = [{term_key:category,weight_key:1}]
    data[part_key] = parts
    return data

categories = get_categories(TEST_CATEGORIES_FILE)
for category in categories:
    data = get_body_create_pool(category,NAME_KEY,DESCRIPTION_KEY,LANGUAGE_KEY,PARTS_KEY,TERM_KEY,WEIGHT_KEY)
    headers = {'Content-type': 'application/json'}
    create_pool_url = BASE_URL + END_URL + AUTH
    create_pool_request = requests.post(create_pool_url, auth=HTTPBasicAuth('vide.karlsson@gmail.com', 'jh2gmoc'), data=json.dumps(data), headers=headers)
    print(create_pool_request.text)
