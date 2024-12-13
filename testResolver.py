import requests
from pprint import pprint

def verify_taxon(nome_taxon:str) -> dict:
    """
    """
    valid_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    url = "http://resolver.globalnames.org/name_resolvers.json"
    params = {
        'names': nome_taxon,
        'best_match_only': True,
        'data_source_ids': 1,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        service = data['data'][0]['results'][0]
        if 'data' in data and data['data']:
            paths = service['classification_path'].split('|')
            ids = service['classification_path_ids'].split('|')
            ranks = service['classification_path_ranks'].split('|')

            result = {}
            for i, rank in enumerate(ranks):
                if rank in valid_ranks:
                    result[rank] = [paths[i], ids[i] if ids != [''] else 'No ID']
            result['scientificName'] = [service['name_string'], service['taxon_id'] if \
                                        service['taxon_id'] != [''] else 'No ID']
                
            for rank in valid_ranks:
                if rank not in result:
                    result[rank] = ['', '']

            return result
        
pprint(verify_taxon('Homo sapiens'))