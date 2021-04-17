import requests
import secrets
import json

def find_id(firstname, lastname, affil):
    url = f'http://api.elsevier.com/content/search/author?query=AUTHFIRST({firstname})+AND+AUTHLASTNAME({lastname})+AND+AFFIL({affil})&apiKey={secrets.key}'
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()

    if data['search-results']['opensearch:totalResults'] == '0':
        return None
    else:
        author_id = data['search-results']['entry'][0]['dc:identifier'][data['search-results']['entry'][0]['dc:identifier'].index(':')+1:]

    return author_id

def retrieve_auth_detail(id):
    url = f'http://api.elsevier.com/content/search/scopus?query=AU-ID({id})&count=100&apiKey={secrets.key}'
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()
    results = []
    for entry in data['search-results']['entry']:
        for link in entry['link']:
            if link['@ref'] == 'scopus':
                ref = link['@href']
                break
        results.append({
            'title': entry['dc:title'],
            'url': ref
        })
    return results
