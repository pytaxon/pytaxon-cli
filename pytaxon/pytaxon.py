import pandas as pd
import requests
from collections import defaultdict
from tqdm import tqdm


class Pytaxon:
    def __init__(self):
        self._spreadsheet:str = None
        self._original_df:pd.DataFrame = None

        # Taxonomy
        self._genus_column:str = None
        self._species_column:str = None
        self._taxons_list:list = None

        self._json_post:dict = None
        self.r = None  # 

        self._matched_names:dict = None
        self._incorrect_taxon_data:defaultdict = defaultdict(list)

        self._df_to_correct:pd.DataFrame = None
        self._corrected_df = None
        self._lineage_dict = dict
        self._incorrect_lineage_data:defaultdict = defaultdict(list)

        # Lineage
        self._lineage_dict:defaultdict = defaultdict(list)
        self._tribe_column:str = None
        self._family_column:str = None
        self._order_column:str = None
        self._class_column:str = None
        self._phylum_column:str = None


    @property
    def logo(self):
        return '''                            \033[33m,d\033[m                                                       
                            \033[33m88\033[m                                                       
\033[32m8b,dPPYba,   8b       d8\033[m\033[33m  MM88MMM  ,adPPYYba,  8b,     ,d8  ,adPPYba,   8b,dPPYba, \033[m  
\033[32m88P'    "8a  `8b     d8'\033[m\033[33m    88     ""     `Y8   `Y8, ,8P'  a8"     "8a  88P'   `"8a\033[m  
\033[32m88       d8   `8b   d8' \033[m\033[33m    88     ,adPPPPP88     )888(    8b       d8  88       88\033[m  
\033[32m88b,   ,a8"    `8b,d8'  \033[m\033[33m    88,    88,    ,88   ,d8" "8b,  "8a,   ,a8"  88       88\033[m  
\033[32m88`YbbdP"'       Y88'   \033[m\033[33m    "Y888  `"8bbdP"Y8  8P'     `Y8  `"YbbdP"'   88       88\033[m  
\033[32m88               d8'    \033[m                                                             
\033[32m88              d8' \033[m
                            Taxonomy and Lineage Checker\n'''
    

    @property
    def menu(self):
        return '''[1] Check TAXONOMIES (species name) and create a pivot
[2] Correct original spreadsheet through pivot
[3] Check LINEAGE and create a pivot
[4] Correct original spreadsheet through pivot
Choose a option: '''


    def read_spreadshet(self, spreadsheet:str) -> None:
        self._spreadsheet = spreadsheet.replace('"', '')
        try:
            self._original_df = pd.read_excel(self._spreadsheet).reset_index()
            print('Success reading the spreadsheet, now entering columns names...')
        except Exception as e:
            print('Error reading the spreadsheet: ', e)  


    #  T A X O N O M I E S
    def read_taxon_columns(self, genus:str, species:str) -> None:
        self._genus_column = genus
        self._species_column = species

        try: 
            self._taxons_list = list((self._original_df[self._genus_column] + ' ' + self._original_df[self._species_column]).values)
            print('Success loading spreadsheet with given columns names, now connecting to API...')
        except Exception as e:
            print('Error loading spreadsheet with given columns names', e)


    def connect_to_api(self) -> None:
        self._json_post = {'names': self._taxons_list,
                           'do_approximate_matching': True,
                           'context_name': 'All life'}

        try:
            self.r = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=self._json_post)
            print('Success accessing the OpenTreeOfLife API, now checking taxons...')
        except Exception as error:
            print('Error accessing the OpenTreeOfLife API: ', error)


    def data_incorrect_taxons(self) -> None:
        self._matched_names = self.r.json()['matched_names']

        for i in tqdm(range(len(self._matched_names)), desc="Checking taxons from original spreadsheet", ncols=100):
            try:
                first_match_score = self.r.json()['results'][i]['matches'][0]['score']
            except:
                self._incorrect_taxon_data['Error Line'].append(self._matched_names.index(self._matched_names[i], i))
                self._incorrect_taxon_data['Wrong Taxon'].append(self._matched_names[i])
                self._incorrect_taxon_data['Options'].append('No Correspondence')
                self._incorrect_taxon_data['Match Score'].append(0)
                self._incorrect_taxon_data['Alternatives'].append(None)
                self._incorrect_taxon_data['Taxon Sources'].append(None)
                continue

            if first_match_score < 1.:
                matches = self.r.json()['results'][i]['matches']
                match_names  = [match['matched_name'] for match in matches]

                self._incorrect_taxon_data['Error Line'].append(self._matched_names.index(self._matched_names[i], i))
                self._incorrect_taxon_data['Wrong Taxon'].append(self._matched_names[i])
                self._incorrect_taxon_data['Options'].append((list(range(1, len(match_names)+1))))
                self._incorrect_taxon_data['Matches Scores'].append([round(match['score'], 3) for match in matches])
                self._incorrect_taxon_data['Alternatives'].append(match_names)
                self._incorrect_taxon_data['Taxon Sources'].append([match['taxon']['tax_sources'] for match in matches])
                continue


    def create_taxonomies_pivot_spreadsheet(self) -> None:
        def sum2(num):
            return num + 2
        
        Alternatives1 = []
        Alternatives2 = []
        for i in tqdm(range(len(self._incorrect_taxon_data['Alternatives'])), desc="Creating pivot spreadsheet", ncols=100):
            result = f"Species Name: {self._incorrect_taxon_data['Alternatives'][i][0]} | Score: {self._incorrect_taxon_data['Matches Scores'][i][0]} | Sources: {self._incorrect_taxon_data['Taxon Sources'][i][0]}"
            result2 = f"Species Name: {self._incorrect_taxon_data['Alternatives'][i][1]} | Score: {self._incorrect_taxon_data['Matches Scores'][i][1]} | Sources: {self._incorrect_taxon_data['Taxon Sources'][i][1]}"
            
            Alternatives1.append(result)
            Alternatives2.append(result2)

        self._df_to_correct = pd.DataFrame(data={  # Refazer
            'Error Line': list(map(sum2, self._incorrect_taxon_data['Error Line'])),
            'Wrong Taxon': self._incorrect_taxon_data['Wrong Taxon'],
            'Options': self._incorrect_taxon_data['Options'],
            'Alternative1': Alternatives1,
            'Alternative2': Alternatives2
            })

        try:
            self._df_to_correct.to_excel(f'{self._spreadsheet[:-4]}_por_corrigir.xlsx')
            print('Success creating pivot spreadsheet!')
        except Exception as e:
            print('Error creating pivot spreadsheet: ', e)


    def update_original_spreadsheet(self):
        corrections = self._df_to_correct['Alternative1'].str.split(expand=True)  # Ajeitar

        self._corrected_df = self._original_df

        self._corrected_df.loc[self._incorrect_taxon_data['Error Line'], self._genus_column] = corrections[1].values
        self._corrected_df.loc[self._incorrect_taxon_data['Error Line'], self._species_column] = corrections[2].values

        try:
            self._corrected_df.to_excel(f'{self._spreadsheet[:-4]}_corrigido.xlsx')
        except Exception as e:
            print('Error to update original spreadsheet: ', e)


    #  L I N E A G E
    def read_lineage_columns(self, tribe, family, order, class_, phylum) -> None:
        self._tribe_column = tribe
        self._family_column = family
        self._order_column = order
        self._class_column = class_
        self._phylum_column = phylum

        df_to_be_used = self._corrected_df if self._corrected_df else self._original_df

        try: 
            self._lineage_dict['tribe'].append(df_to_be_used[self._tribe_column])
            self._lineage_dict['family'].append(df_to_be_used[self._family_column])
            self._lineage_dict['order'].append(df_to_be_used[self._order_column])
            self._lineage_dict['class_'].append(df_to_be_used[self._class_column])
            self._lineage_dict['phylum'].append(df_to_be_used[self._phylum_column])

            print('Success loading spreadsheet with given columns names, now connecting to API...')
        except Exception as e:
            print('Error loading spreadsheet with given columns names', e)
