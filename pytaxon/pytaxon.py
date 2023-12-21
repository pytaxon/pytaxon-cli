import os
import time
import ast
from collections import defaultdict

import pandas as pd
from tqdm import tqdm
import requests


class Pytaxon:
    def __init__(self):
        self._original_df:pd.DataFrame = None
        self._incorrect_data:defaultdict = defaultdict(list)

        print(self.logo)

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

    def connect_to_api(self, link, service_name) -> None:        
        if requests.get(link).status_code != 200 if service_name == 'GBIF' else requests.get(link).status_code == 200:  # TO FIX
            print(f"Could not connect to {service_name} api")
            exit()
        else:
            print(f"Connected to {service_name} api")
        time.sleep(1)

    def read_spreadshet(self, original_spreadsheet:str) -> tuple:
        original_spreadsheet_path = original_spreadsheet.replace('"', '')
        original_spreadsheet = os.path.basename(original_spreadsheet_path)
        original_spreadsheet_name, _ = os.path.splitext(original_spreadsheet)

        self._original_df = pd.read_excel(original_spreadsheet_path).\
            reset_index().fillna('')[:30]  # TO CHANGE

        print(f'Spreadsheet {original_spreadsheet_name} read.')
        time.sleep(1)

        return self._original_df

    def read_columns(self, column_vars:list) -> None:
        self.column_vars = ast.literal_eval(column_vars)

        missing_columns = [column for column in self.column_vars if column not in self._original_df.columns]

        if not missing_columns:
            print('Columns choosed.')
        else:
            print(f"The following columns were not found: {', '.join(missing_columns)}")
            exit()
     
    def compare_data(self, append_ID_number, line, column_error, wrong_data, corrected_data, id_number) -> bool:
            if corrected_data != wrong_data:
                self._incorrect_data['Error Line'].append(line)
                self._incorrect_data['Error Type'].append(column_error)
                self._incorrect_data['Wrong Name'].append(wrong_data)
                self._incorrect_data['Suggested Name'].append(corrected_data)
                append_ID_number()
                self._incorrect_data['Change'].append('y/n')

    def create_to_correct_spreadsheet(self, spreadsheet_name):
        if self._incorrect_data:
            to_correct_df = pd.DataFrame(self._incorrect_data).style.map(
                lambda x: 'color: blue; text-decoration: underline;',
                subset=self.source_id,
            )

            to_correct_df.to_excel(f'{spreadsheet_name}.xlsx')
        else:
            print('No errors in spreadsheet')

    def update_original_spreadsheet(self, original_spreadsheet:str, to_correct_spreadsheet:str, spreadsheet_name:str):
        original_data_df = self.read_spreadshet(original_spreadsheet)
        to_correct_df = self.read_spreadshet(to_correct_spreadsheet)

        for index, row in to_correct_df.iterrows():
            if row['Change'] == 'y':
                original_data_df.at[row['Error Line']-2, row['Error Type']] = row['Suggested Name']
        
        self._corrected_spreadsheet = original_data_df.copy()

        try:
            self._corrected_spreadsheet.to_excel(f'{spreadsheet_name}.xlsx')
        except Exception as e:
            print('Error to update original spreadsheet: ', e)


class Pytaxon_OTT(Pytaxon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect_to_api('https://api.opentreeoflife.org/v3/tnrs/match_names', 'OTT')

    def compare_data(self, line, column_error, wrong_data, corrected_data, id_number) -> bool:
        def append_ID_number():
            self._incorrect_data['OTT ID Source'].append(f'=HYPERLINK("https://tree.opentreeoflife.org/taxonomy/browse?id={id_number}", "{id_number}")')
        super().compare_data(append_ID_number, line, column_error, wrong_data, corrected_data, id_number)

    def check_species_and_lineage(self) -> None:
        species_list = self._original_df[self.column_vars[0]]

        for counter in tqdm(range(len(species_list))):
            if species_list[counter] == '':
                continue

            json_name = {'names': [species_list[counter]],
                        'do_approximate_matching': True,
                        'context_name': 'All life'}
            r_name = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=json_name)
            ott_id = r_name.json()['results'][0]['matches'][0]['taxon']['ott_id']
            json_id = {'ott_id': ott_id, 'include_lineage': True}
            r_id = requests.post('https://api.opentreeoflife.org/v3/taxonomy/taxon_info', json=json_id)
            lineage = r_id.json()['lineage']
            c = 1 if len(lineage) == 33 else 0

            self.compare_data(counter+2, self.column_vars[0], self._original_df[self.column_vars[0]][counter], r_name.json()['results'][0]['matches'][0]['matched_name'], r_name.json()['results'][0]['matches'][0]['taxon']['ott_id'])  # species
            self.compare_data(counter+2, self.column_vars[1], self._original_df[self.column_vars[1]][counter], lineage[3 + c]['unique_name'], lineage[3 + c]['ott_id'])  # family
            self.compare_data(counter+2, self.column_vars[2], self._original_df[self.column_vars[2]][counter], lineage[10 + c]['unique_name'], lineage[10 + c]['ott_id'])  # order
            self.compare_data(counter+2, self.column_vars[3], self._original_df[self.column_vars[3]][counter], lineage[16 + c]['unique_name'], lineage[16 + c]['ott_id'])  # class
            self.compare_data(counter+2, self.column_vars[4], self._original_df[self.column_vars[4]][counter], lineage[20 + c]['unique_name'], lineage[20 + c]['ott_id'])  # phylum

    def create_to_correct_spreadsheet(self, spreadsheet_name):
        self.source_id = ['OTT ID Source']
        super().create_to_correct_spreadsheet(spreadsheet_name)


class Pytaxon_GBIF(Pytaxon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect_to_api('https://api.gbif.org/v1/species/match', 'GBIF')

    def compare_data(self, line, column_error, wrong_data, corrected_data, id_number) -> bool:
        def append_ID_number():
            self._incorrect_data['GBIF ID Source'].append(f'=HYPERLINK("https://www.gbif.org/species/{id_number}", "{id_number}")')
        super().compare_data(append_ID_number, line, column_error, wrong_data, corrected_data, id_number)

    def check_species_and_lineage(self):
        species_list = self._original_df[self.column_vars[0]]
        for counter in tqdm(range(len(species_list))):
            if species_list[counter] == '':
                continue

            json_post = {'name': species_list[counter],
                         'verbose': True}

            r = requests.get('https://api.gbif.org/v1/species/match', params=json_post)

            self.compare_data(counter+2, self.column_vars[0], self._original_df[self.column_vars[0]][counter], r.json()['species'], r.json()['speciesKey'])  # species
            self.compare_data(counter+2, self.column_vars[1], self._original_df[self.column_vars[1]][counter], r.json()['family'], r.json()['familyKey'])  # family
            self.compare_data(counter+2, self.column_vars[2], self._original_df[self.column_vars[2]][counter], r.json()['order'], r.json()['orderKey'])  # order
            self.compare_data(counter+2, self.column_vars[3], self._original_df[self.column_vars[3]][counter], r.json()['class'], r.json()['classKey'])  # class
            self.compare_data(counter+2, self.column_vars[4], self._original_df[self.column_vars[4]][counter], r.json()['phylum'], r.json()['phylumKey'])  # phylum
            self.compare_data(counter+2, self.column_vars[5], self._original_df[self.column_vars[5]][counter], r.json()['kingdom'], r.json()['kingdomKey'])  # kingdom

    def create_to_correct_spreadsheet(self, spreadsheet_name):
        self.source_id = ['GBIF ID Source']
        super().create_to_correct_spreadsheet(spreadsheet_name)
