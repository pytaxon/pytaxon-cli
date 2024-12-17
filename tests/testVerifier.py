import requests
from pprint import pprint

url = "https://verifier.globalnames.org/api/v1/verifications"
valid_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

payload = {
    "nameStrings": [
        'Thelyphonidae'
    ],
    "dataSources": [
        1
    ],
    "withAllMatches": False,
    "withCapitalization": False,
    "withSpeciesGroup": False,
    "withUninomialFuzzyMatch": False,
    "withStats": True,
    "mainTaxonThreshold": 0.6
    }

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    pprint(response.json())
    print()

except requests.RequestException as e:
    print(f"Erro ao acessar a API: {e}")
    print(None)

if response.status_code == 200:
    data = response.json()
    service = data['names'][0]['bestResult']
    paths = service['classificationPath'].split('|')
    ids = service['classificationIds'].split('|')
    ranks = service['classificationRanks'].split('|')

    result = {}
    for i, rank in enumerate(ranks):
        if rank in valid_ranks:
            result[rank] = [paths[i], ids[i] if ids != [''] else 'No ID']
    result['scientificName'] = [service['matchedCanonicalSimple'], service['recordId'] if \
                                service['recordId'] != [''] else 'No ID']
        
    for rank in valid_ranks:
        if rank not in result:
            result[rank] = ['', '']

    pprint(result)