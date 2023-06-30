import pandas as pd
import numpy as np
import requests

class Pytaxon:
    def __init__(self, spreadsheet, column1, column2):
        self._spreadsheet = spreadsheet
        self._column1 = column1
        self._column2 = column2

        json_post = {'names': self.read_spreadshet_to_taxon_list(), 
                     'do_approximate_matching': True, 
                     'context_name': 'All life'}
        
        try:
            self.r = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=json_post)
        except Exception as error:
            print(error)

    def read_spreadshet_to_taxon_list(self) -> list:
        df = pd.read_excel(self._spreadsheet)

        return list((df[self._column1] + ' ' + df[self._column2]).values)
    
    def incorrect_taxons(self):
        matched_names = self.r.json()['matched_names']
        for i, taxon in enumerate(matched_names):
            try:
                first_match_score = self.r.json()['results'][i]['matches'][0]['score']
            except:
                yield [match_index, taxon, 'No Correspondence']
            
            if first_match_score != 1.0:
                matches = self.r.json()['results'][i]['matches']

                match_index = matched_names.index(taxon, i)
                match_name  = [match['matched_name'] for match in matches]
                match_score = [round(match['score'], 3) for match in matches]
                
                yield [match_index, taxon, match_name, match_score]

    def read_report(self):
        report = list(self.incorrect_taxons())
        # print(report)

        df = pd.DataFrame(data={
            'index': [i[0] for i in report],
            'wrong_taxon': [i[1] for i in report],
            'alternative_1': [[i[2][0], i[3][0]] for i in report],
            'alternative_2': [[i[2][1], i[3][1]] for i in report]
            })
        
        print(df)
        df.to_excel(f'{self._spreadsheet[:-4]}_anotado.xlsx')

pt = Pytaxon('db/Lepidoptera_-_Importacao_IX_lote_1.xls', 'Genus1', 'Species1')
pt.read_report()
