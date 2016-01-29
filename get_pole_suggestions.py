import json
import requests
from requests.auth import HTTPBasicAuth

import pickle_handler
POLES_KEY = 'poles'
ID_KEY = 'id'
POLES_PART_KEY = "parts"
TERM_KEY = "term"
SUGGESTIONS_KEY ="suggestions"

BASE_URL = 'https://ethersource.gavagai.se/ethersource/rest/v2/poles'
END_URL = '?'
AUTH = 'apiKey=123'
SUGGEST_URL = '/suggest'
#/1037/suggest?apiKey=123

ALL_CATEGORIES_FILE = 'all_categories.txt'

all_categories = []
with open(ALL_CATEGORIES_FILE) as f:
    all_categories = f.readlines()

all_categories = [category.rstrip() for category in all_categories]
all_categories = set(all_categories)

get_poles_request = requests.get('https://ethersource.gavagai.se/ethersource/rest/v2/poles'+END_URL+AUTH, auth=HTTPBasicAuth('vide.karlsson@gmail.com', 'jh2gmoc'))
response_get_poles = json.loads(get_poles_request.text)
# print(response_get_poles)

list_of_poles = response_get_poles[POLES_KEY]
list_of_pole_id = []
for pole in list_of_poles:
    pole_id = pole[ID_KEY]
    list_of_pole_id.append(pole_id)

# print(list_of_pole_id)
import pdb
pdb.set_trace()
list_of_pole_info = []
category_pole_id_map = {}
for pole_id in list_of_pole_id:
    get_pole_info_url = BASE_URL + '/' + str(pole_id) + END_URL + AUTH
    get_pole_info_request = requests.get(get_pole_info_url, auth=HTTPBasicAuth('vide.karlsson@gmail.com', 'jh2gmoc'))
    response_pole_info = json.loads(get_pole_info_request.text)
    term = response_pole_info[POLES_PART_KEY][0][TERM_KEY]
    if term in all_categories and len(response_pole_info[POLES_PART_KEY]) == 1:
        category_pole_id_map[term] = pole_id
        print(term)

category_gavagai_cosine_similare_sugestions_map = {}
category_gavagai_sting_similare_sugestions_map = {}

for category in category_pole_id_map:
    pole_id = category_pole_id_map[category]
    get_suggestions_url = BASE_URL + '/' + str(pole_id)+ SUGGEST_URL + END_URL + AUTH
    get_suggestions_request = requests.get(get_suggestions_url, auth=HTTPBasicAuth('vide.karlsson@gmail.com', 'jh2gmoc'))
    get_suggestions_respons = json.loads(get_suggestions_request.text)
    suggestions = get_suggestions_respons[SUGGESTIONS_KEY]
    category_gavagai_sting_similare_sugestions_map[category] = []
    category_gavagai_cosine_similare_sugestions_map[category] = []
    for suggestion in suggestions:
        if suggestion['sumCosine'] > 0 and suggestion['stringSimilarity'] == False:
            category_gavagai_cosine_similare_sugestions_map[category].append(suggestion)
        if suggestion['stringSimilarity'] == True:
            category_gavagai_sting_similare_sugestions_map[category].append(suggestion)
    print(category)        

pickle_handler.print_pickle(category_gavagai_cosine_similare_sugestions_map, 'gavagai_cosinus_similare_terms')
pickle_handler.print_pickle(category_gavagai_sting_similare_sugestions_map, 'gavagai_string_similare_terms')



