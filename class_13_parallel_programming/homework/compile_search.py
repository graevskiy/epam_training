
import requests
import json

googl_url = "https://serpapi.com/search"
search = {'q': 'apple', 'tbm': 'isch'}

with requests.get(googl_url, params=search) as r:
    res = r.json()

with open('urls_google.txt', 'w', encoding='utf-8') as f:
    for i in res['images_results']:
        if 'original' in i:
            f.write(f"{i['original']}\n")