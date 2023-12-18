import os
from collections import defaultdict
from pprint import pprint
import time

import pandas as pd
import requests
from tqdm import tqdm
from thefuzz import process


class Pytaxon_GBIF:
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
        self.connect_to_GBIF_api()


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
                         Taxonomy and Lineage Checker - GBIF API\n'''
    

    @property
    def menu(self):
        return '''[1] Check SPECIES NAME and LINEAGE then create a pivot
[2] Correct original spreadsheet through pivot
Choose a option: '''


    def connect_to_GBIF_api(self) -> None:
        if  requests.get('https://api.gbif.org/v1/species/match').status_code != 200:
            print("Could not connect to GBIF api")
            exit()
        else:
            print("Connected to GBIF api")
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
        self.kingdom_column_name = process.extractOne("kingdom", self._original_df.columns)[0]
        self.phylum_column_name = process.extractOne("phylum", self._original_df.columns)[0]
        self.class_column_name = process.extractOne("class", self._original_df.columns)[0]
        self.order_column_name = process.extractOne("order", self._original_df.columns)[0]
        self.family_column_name = process.extractOne("family", self._original_df.columns)[0]

        print('Columns choosed.')


    def check_species_and_lineage(self) -> None:

        def compare_data(line, column_error, wrong_data, corrected_data, id_number) -> bool:
            """
            Compares the wrong data with the corrected data and updates the `_incorrect_data` dictionary if they are different.

            Args:
                line: The line number of the error.
                column_error: Which column has the error.
                wrong_data: The wrong data.
                corrected_data: The corrected data.

            Returns:
                bool: True if the corrected data is different from the wrong data, False otherwise.
            """
            if corrected_data != wrong_data:
                self._incorrect_data['Error Line'].append(line)
                self._incorrect_data['Error Type'].append(column_error)
                self._incorrect_data['Wrong Data'].append(wrong_data)
                self._incorrect_data['Corrected Data'].append(corrected_data)
                self._incorrect_data['ID Number'].append(f'=HYPERLINK("https://www.gbif.org/species/{id_number}", "{id_number}")')
                self._incorrect_data['Change'].append('y/n')

        species_list = self._original_df[self.species_column_name]
        # self._taxons_list = list((self._original_df[self._genus_column] + ' ' + self._original_df[self._species_column]).values)  FOR TEST

        for counter in tqdm(range(len(species_list))):
            if species_list[counter] == '':
                continue

            json_post = {'name': species_list[counter],
                         'verbose': True}

            r = requests.get('https://api.gbif.org/v1/species/match', params=json_post)

            compare_data(counter+2, self.species_column_name, self._original_df[self.species_column_name][counter], r.json()['species'], r.json()['speciesKey'])  # species
            compare_data(counter+2, self.kingdom_column_name, self._original_df[self.kingdom_column_name][counter], r.json()['kingdom'], r.json()['kingdomKey'])  # kingdom
            compare_data(counter+2, self.phylum_column_name, self._original_df[self.phylum_column_name][counter], r.json()['phylum'], r.json()['phylumKey'])  # phylum
            compare_data(counter+2, self.class_column_name, self._original_df[self.class_column_name][counter], r.json()['class'], r.json()['classKey'])  # class
            compare_data(counter+2, self.order_column_name, self._original_df[self.order_column_name][counter], r.json()['order'], r.json()['orderKey'])  # order
            compare_data(counter+2, self.family_column_name, self._original_df[self.family_column_name][counter], r.json()['family'], r.json()['familyKey'])  # family

        if self._incorrect_data:
            self._to_correct_df = pd.DataFrame(self._incorrect_data).style.map(
                lambda x: 'color: blue; text-decoration: underline;',
                subset=['ID Number'],
            )

            self._to_correct_df.to_excel(f'TO_CORRECT_{self._original_spreadsheet_name}.xlsx')
        else:
            print('No errors in spreadsheet')


    def update_original_spreadsheet(self, original_spreadsheet:str, to_correct_spreadsheet:str):
        original_data_name, original_data_df = self.read_spreadshet(original_spreadsheet)
        to_correct_data_name, to_correct_df = self.read_spreadshet(to_correct_spreadsheet)

        for index, row in to_correct_df.iterrows():
            if row['Change'] == 'y':
                original_data_df.at[row['Error Line']-2, row['Error Type']] = row['Corrected Data']
        
        self._corrected_spreadsheet = original_data_df.copy()

        try:
            self._corrected_spreadsheet.to_excel(f'CORRECTED_{original_data_name}.xlsx')
        except Exception as e:
            print('Error to update original spreadsheet: ', e)
