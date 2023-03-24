import pprint
import json
import requests
from front import print_bonito

print_bonito()
# pp = pprint.PrettyPrinter(indent=4)
url = 'http://resolver.globalnames.org/name_resolvers.json'
df = {}
nomes_avaliados = input('Digite o nome a ser avaliado (para mais de um, usar "|"): ')
nomes = nomes_avaliados.split('|')

try:
    r = requests.get(url, params={'names': nomes_avaliados})
    # pp.pprint(r.json()['data'][1])
    for i, nome in enumerate(nomes):
        nomes_taxon = r.json()['data'][i]
    
        print(f'{nome} consta no BD? {nomes_taxon["is_known_name"]}')

        df[nome] = [i['canonical_form'] for i in nomes_taxon['results']]

    # df = pd.DataFrame(df, index=[nomes])    

    print(df)
    # df.to_excel('teste.xlsx')

except:
    print('erro de conexão com a API')
