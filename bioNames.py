import requests
from front import logo_bionames

logo_bionames()
nome_avaliado = input('Digite o nome a ser avaliado: ')
url = f'https://bionames.org/api/name/{nome_avaliado}/didyoumean'

try:
    r = requests.get(url, params={'names': nome_avaliado})

    nomes_equivalentes = r.json()['names']
    for nome in nomes_equivalentes:
        print(nome)
except:
    print('ERRO')
