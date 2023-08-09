import pandas as pd
import requests
from collections import defaultdict

class Pytaxon:
    def __init__(self, spreadsheet:str=False):
        self._spreadsheet:str = spreadsheet.replace('"', '')
        self._original_df:pd.DataFrame = None
        self._column1:str = None
        self._column2:str = None
        self._taxons_list:list = None
        self._json_post:dict = None
        self._matched_names:dict = None
        self._incorrect_taxon_data:dict = None
        self._df_to_correct:pd.DataFrame = None

        if self._spreadsheet:
            self.read_spreadshet()
        # else:
        #     self.update_original_spreadsheet()

    def read_spreadshet(self) -> None:
        try:
            self._original_df = pd.read_excel(self._spreadsheet).reset_index()
            print('Succes reading the spreadsheet, now entering columns names...')
            self.enter_columns_names()   
        except Exception as e:
            print('Error reading the spreadsheet: ', e)

    def enter_columns_names(self) -> None:
        self._column1, self._column2 = input('Digit the name of the Genus and Species columns: ').split()

        try: 
            self._taxons_list = list((self._original_df[self._column1] + ' ' + self._original_df[self._column2]).values)
            print('Success loading spreadsheet with given columns names, now connecting to API...')
            self.connect_to_api()
        except Exception as e:
            print('Error loading spreadsheet with given columns names', e)

    def connect_to_api(self) -> None:
        self._json_post = {'names': self._taxons_list,
                           'do_approximate_matching': True,
                           'context_name': 'All life'}

        try:
            self.r = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=self._json_post)
            print('Success accessing the OpenTreeOfLife API, now checking taxons...')
            self.incorrect_taxons()
        except Exception as error:
            print('Error accessing the OpenTreeOfLife API: ', error)

    def incorrect_taxons(self) -> None:
        self._matched_names = self.r.json()['matched_names']
        self._incorrect_taxon_data = defaultdict(list)

        for i, taxon in enumerate(self._matched_names):
            try:
                first_match_score = self.r.json()['results'][i]['matches'][0]['score']
            except:
                self._incorrect_taxon_data['Error Line'].append(self._matched_names.index(taxon, i))
                self._incorrect_taxon_data['Wrong Taxon'].append(taxon)
                self._incorrect_taxon_data['Options'].append('No Correspondence')
                self._incorrect_taxon_data['Match Score'].append(0)
                self._incorrect_taxon_data['Alternatives'].append(None)
                continue

            if first_match_score < 1.:
                matches = self.r.json()['results'][i]['matches']
                match_names  = [match['matched_name'] for match in matches]

                self._incorrect_taxon_data['Error Line'].append(self._matched_names.index(taxon, i))
                self._incorrect_taxon_data['Wrong Taxon'].append(taxon)
                self._incorrect_taxon_data['Options'].append((list(range(1, len(match_names)+1))))
                self._incorrect_taxon_data['Matches Scores'].append([round(match['score'], 3) for match in matches])
                self._incorrect_taxon_data['Alternatives'].append(match_names)
                continue

        self.create_pivot_spreadsheet()
        # pprint(dict(self._incorrect_taxon_data))

    def create_pivot_spreadsheet(self) -> None:
        def sum2(num):
            return num + 2
        
        # Ajeitar
        Alternatives1 = []
        Alternatives2 = []
        for i in range(len(self._incorrect_taxon_data['Alternatives'])):
            result = f"Taxon:{self._incorrect_taxon_data['Alternatives'][0][i]} | Score:{self._incorrect_taxon_data['Matches Scores'][0][i]}"
            result2 = f"Taxon:{self._incorrect_taxon_data['Alternatives'][1][i]} | Score:{self._incorrect_taxon_data['Matches Scores'][1][i]}"
            Alternatives1.append(result)
            Alternatives2.append(result2)
        
        self._df_to_correct = pd.DataFrame(data={  # Refazer
            'Error Line': list(map(sum2, self._incorrect_taxon_data['Error Line'])),
            'Wrong Taxon': self._incorrect_taxon_data['Wrong Taxon'],
            'Options': self._incorrect_taxon_data['Options'],
            'Alternative1': [data for data in Alternatives1],  # Ajeitar
            'Alternative2': [data for data in Alternatives2]  # Ajeitar
            })

        print(self._df_to_correct)
        self._df_to_correct.to_excel(f'{self._spreadsheet[:-4]}_por_corrigir.xlsx')
        self.update_original_spreadsheet()

    def update_original_spreadsheet(self):
        corrections = self._df_to_correct['Alternative1'].str.split(expand=True)  # Ajeitar
        self._original_df.loc[self._incorrect_taxon_data['Error Line'], self._column1] = corrections[0].values
        self._original_df.loc[self._incorrect_taxon_data['Error Line'], self._column2] = corrections[1].values

        try:
            self._original_df.to_excel(f'{self._spreadsheet[:-4]}_corrigido.xlsx')
        except Exception as e:
            print('Error to update original spreadsheet: ', e)
