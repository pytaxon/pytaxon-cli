import os
from collections import defaultdict
from pprint import pprint

import pandas as pd
import requests
from tqdm import tqdm
from thefuzz import process
import time


class Pytaxon_OTT:
    def __init__(self):
        self._original_spreadsheet_path:str = None
        self._original_spreadsheet:str = None
        self._original_spreadsheet_name:str = None
        self._original_df:pd.DataFrame = None

        self._species_column:str = None
        self._kingdom_column:str = None
        self._phylum_column:str = None
        self._class_column:str = None
        self._order_column:str = None
        self._family_column:str = None
        self._incorrect_data:defaultdict = defaultdict(list)

        print(self.logo)
        self.connect_to_OTT_api()


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
                         Taxonomy and Lineage Checker - OTT API\n'''
    

    @property
    def menu(self):
        return '''[1] Check TAXONOMIES (species name) and create a pivot
[2] Correct original spreadsheet through pivot
[3] Check LINEAGE and create a pivot
[4] Correct original spreadsheet through pivot
Choose a option: '''


    def connect_to_OTT_api(self) -> None:        
        if requests.get('https://api.opentreeoflife.org/v3/tnrs/match_names').status_code == 200: 
            print("Could not connect to OTT api")
            exit()
        else:
            print("Connected to OTT api")
        time.sleep(1)


    def read_spreadshet(self, original_spreadsheet:str) -> tuple:
        original_spreadsheet_path = original_spreadsheet.replace('"', '')
        original_spreadsheet = os.path.basename(original_spreadsheet_path)
        self._original_spreadsheet_name, _ = os.path.splitext(original_spreadsheet)

        self._original_df = pd.read_excel(original_spreadsheet_path).\
            reset_index().fillna('')[:30]  # CHANGE

        print(f'Spreadsheet {self._original_spreadsheet_name} read.')
        time.sleep(1)

        return self._original_spreadsheet_name, self._original_df


    def read_columns(self) -> None:
        self.species_column_name = process.extractOne("species", self._original_df.columns)[0]
        self.phylum_column_name = process.extractOne("phylum", self._original_df.columns)[0]
        self.class_column_name = process.extractOne("class", self._original_df.columns)[0]
        self.order_column_name = process.extractOne("order", self._original_df.columns)[0]
        self.family_column_name = process.extractOne("family", self._original_df.columns)[0]

        print('Columns choosed.')

     
    def check_species_and_lineage(self) -> None:

            def compare_data(line, column_error, wrong_data, corrected_data, id_number) -> bool:
                if corrected_data != wrong_data:
                    self._incorrect_data['Error Line'].append(line)
                    self._incorrect_data['Error Type'].append(column_error)
                    self._incorrect_data['Wrong Name'].append(wrong_data)
                    self._incorrect_data['Suggested Name'].append(corrected_data)
                    self._incorrect_data['ID Source'].append(f'=HYPERLINK("https://tree.opentreeoflife.org/taxonomy/browse?id={id_number}", "OTT: {id_number}")')
                    self._incorrect_data['Change'].append('y/n')

            species_list = self._original_df[self.species_column_name]

            for counter in tqdm(range(len(species_list))):
                if species_list[counter] == '':
                    continue

                json_post = {'names': [species_list[counter]],
                            'do_approximate_matching': True,
                            'context_name': 'All life'}

                r_name = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=json_post)
                
                ott_id = r_name.json()['results'][0]['matches'][0]['taxon']['ott_id']
                
                _json_post = {'ott_id': ott_id, 'include_lineage': True}

                r_id = requests.post('https://api.opentreeoflife.org/v3/taxonomy/taxon_info', json=_json_post)

                lineage = r_id.json()['lineage']
                c = 1 if len(lineage) == 33 else 0

                compare_data(counter+2, self.species_column_name, self._original_df[self.species_column_name][counter], r_name.json()['results'][0]['matches'][0]['matched_name'], r_name.json()['results'][0]['matches'][0]['taxon']['ott_id'])  # species
                compare_data(counter+2, self.phylum_column_name, self._original_df[self.phylum_column_name][counter], lineage[20 + c]['unique_name'], lineage[20 + c]['ott_id'])  # phylum
                compare_data(counter+2, self.class_column_name, self._original_df[self.class_column_name][counter], lineage[16 + c]['unique_name'], lineage[16 + c]['ott_id'])  # class
                compare_data(counter+2, self.order_column_name, self._original_df[self.order_column_name][counter], lineage[10 + c]['unique_name'], lineage[10 + c]['ott_id'])  # order
                compare_data(counter+2, self.family_column_name, self._original_df[self.family_column_name][counter], lineage[3 + c]['unique_name'], lineage[3 + c]['ott_id'])  # family

            if self._incorrect_data:
                self._to_correct_df = pd.DataFrame(self._incorrect_data).style.map(
                    lambda x: 'color: blue; text-decoration: underline;',
                    subset=['ID Number'],
                )

                self._to_correct_df.to_excel(f'TO_CORRECT_{self._original_spreadsheet_name}.xlsx')
            else:
                print('No errors in spreadsheet')
