import requests
from front import logo_bionames
from excel_reader import read_two_columns_excel

logo_bionames()
# nome_avaliado = input('Digite o nome a ser avaliado: ')
# url = f'https://bionames.org/api/name/{nome_avaliado}/didyoumean'

# try:
#     r = requests.get(url, params={'names': nome_avaliado})

#     nomes_equivalentes = r.json()['names']
#     for nome in nomes_equivalentes:
#         print(nome)
# except:
#     print('ERRO')

# '''
# [1] Digitar nomes
# [2] Importar planilha
# Escolha: '''

for i in read_two_columns_excel('Genus1', 'Species1', 'Lepidoptera_-_Importacao_IX_lote_1.xls'):
    print(f'Táxon a ser identificado: {i}')

    url = f'https://bionames.org/api/name/{i}/didyoumean'

    try:
        r = requests.get(url, params={'names': i})

        nomes_equivalentes = r.json()['names']
        for nome in nomes_equivalentes:
            print(nome)
            
        print('-=' * 24)

    except:
        print('ERRO')
