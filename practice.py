import requests

api_key = 'b95a1c04-ce53-4f95-859b-8e6863a8741f'
word = 'potato'
url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'
res = requests.get(url)
definitions = res.json()
for definition in definitions :
    print(definition)