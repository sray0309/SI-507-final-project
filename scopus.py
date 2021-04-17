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

def retrieve_auth_info(id):
    url = f'http://api.elsevier.com/content/author?author_id={id}&view=metrics&apiKey={secrets.key}'
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()
    if data['author-retrieval-response'][0]['@status'] == 'found':
        info = {
            'h-index': data['author-retrieval-response'][0]['h-index'],
            'coauthor-count': data['author-retrieval-response'][0]['coauthor-count'],
            'document-count': data['author-retrieval-response'][0]['coredata']['document-count'],
            'cited-by-count': data['author-retrieval-response'][0]['coredata']['cited-by-count'],
            'citation-count': data['author-retrieval-response'][0]['coredata']['citation-count']
        }
        return info
    else:
        return None

def retrieve_auth_detail(id, count):
    url = f'http://api.elsevier.com/content/search/scopus?query=AU-ID({id})&field=dc:identifier,dc:title&count={count}&apiKey={secrets.key}'
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()
    print(data['search-results']['entry'])

id = find_id('david', 'blaauw', 'michigan')
print(id)
print(retrieve_auth_info(id))
retrieve_auth_detail(id,1)