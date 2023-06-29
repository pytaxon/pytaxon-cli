import requests
from pprint import pprint
from spreedsheet_reader import read_two_columns_excel

# ['Archaeoprepona amfimarcus', 'Homo sapiensis', 'Homo sapiens', 'abndiuabidunawoiun'],
# 
json_post = {'names': read_two_columns_excel('db/Lepidoptera_-_Importacao_IX_lote_1.xls', 'Genus1', 'Species1'), 
             'do_approximate_matching': True, 
             'context_name': 'All life'}

try:
    r = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=json_post)
    # pprint(r.json())
except:
    print('ERRO')

matched_names = r.json()['matched_names']
for i, taxon in enumerate(matched_names):
    first_match_score = r.json()['results'][i]['matches'][0]['score']
    # r.json()['results'][i]['matches'][0]['is_approximate_match']

    if first_match_score == 1.0:
        print(f"\033[32m{taxon}\033[m")
    else:
        print(f"\033[31m{taxon}\033[m:", end=' ')

        matches = r.json()['results'][i]['matches']
        print([[match['matched_name'], round(match['score'], 3)] for match in matches])
