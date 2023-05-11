import pprint
import json
import requests
from front import logo_global_names_resolver

logo_global_names_resolver()
url = 'http://resolver.globalnames.org/name_resolvers.json'
df = {}
nomes_avaliados = input('Digite o nome a ser avaliado (para mais de um, usar "|"): ')
nomes = nomes_avaliados.split('|')

try:
    r = requests.get(url, params={'names': nomes_avaliados})
    for i, nome in enumerate(nomes):
        nomes_taxon = r.json()['data'][i]
    
        print(f'{nome} consta no banco de dados? {nomes_taxon["is_known_name"]}')

        df[nome] = [i['canonical_form'] for i in nomes_taxon['results']]

    for taxons, dbtaxons in df.items():
        print(f'Nome buscado: {taxons}')
        for a in dbtaxons:
            print(a)
except:
    print('ERRO')
