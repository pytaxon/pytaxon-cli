import os
from collections import defaultdict
from pprint import pprint

import pandas as pd
import requests
from tqdm import tqdm
from thefuzz import process


class Pytaxon_GBIF:
    # GBIF API
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

        self._matched_names:dict = None
        self._incorrect_taxon_data:defaultdict = defaultdict(list)

        self._df_to_correct:pd.DataFrame = None
        self._corrected_df = None
        self._lineage_dict = dict
        self._incorrect_lineage_data:defaultdict = defaultdict(list)

        # Lineage
        self._lineage_dict:defaultdict = defaultdict(list)  #
        

        self.incorrect_lineage_data = defaultdict(list)


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


    def connect_to_api(self) -> None:
        if requests.get('https://api.gbif.org/v1/species/match').status_code() == 200: 
            True
        else: 
            False


    def read_spreadshet(self, original_spreadsheet:str) -> None:
        self._original_spreadsheet_path = original_spreadsheet.replace('"', '')
        self._original_spreadsheet = os.path.basename(self._original_spreadsheet_path)
        self._original_spreadsheet_name, _ = os.path.splitext(self._original_spreadsheet)

        self._original_df = pd.read_excel(self._original_spreadsheet_path).\
            reset_index().fillna('xxxxx')[:1000]  # CHANGE

        print('Spreadsheet read.')


    def read_columns(self,) -> None:
        self.species_column = process.extractOne("species", self._original_df.columns)
        self.kingdom_column = process.extractOne("kingdom", self._original_df.columns)
        self.phylum_column = process.extractOne("phylum", self._original_df.columns)
        self.class_column = process.extractOne("class", self._original_df.columns)
        self.order_column = process.extractOne("order", self._original_df.columns)
        self.family_column = process.extractOne("family", self._original_df.columns)

        # TODO: make a better print for columns and columns input if error
        print('Columns choosed.')


    def check_species_and_lineage(self) -> None:

        def compare_data(line, column_error, wrong_data, corrected_data) -> bool:
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
                self._incorrect_data['Change'].append('y/n')

        species_list = self._original_df[self.species_column[0]]
        # self._taxons_list = list((self._original_df[self._genus_column] + ' ' + self._original_df[self._species_column]).values)  FOR TEST

        for counter in tqdm(range(len(species_list))):
            if species_list[counter] == 'xxxxx':
                continue

            json_post = {'name': species_list[counter],
                         'verbose': True}

            r = requests.get('https://api.gbif.org/v1/species/match', params=json_post)

            compare_data(counter+2, self.species_column, self._original_df[self.species_column[0]][counter], r.json()['species'])  # species
            compare_data(counter+2, self.kingdom_column, self._original_df[self.kingdom_column[0]][counter], r.json()['kingdom'])  # kingdom
            compare_data(counter+2, self.phylum_column, self._original_df[self.phylum_column[0]][counter], r.json()['phylum'])  # phylum
            compare_data(counter+2, self.class_column, self._original_df[self.class_column[0]][counter], r.json()['class'])  # class
            compare_data(counter+2, self.order_column, self._original_df[self.order_column[0]][counter], r.json()['order'])  # order
            compare_data(counter+2, self.family_column, self._original_df[self.family_column[0]][counter], r.json()['family'])  # family

        if self._incorrect_data:
            pd.DataFrame(self._incorrect_data).to_excel(f'TO_CORRECT_{self._original_spreadsheet_name[:-4]}.xlsx')
        else:
            print('No errors in spreadsheet')


    # def update_original_spreadsheet(self, original_spreadsheet:str, _to_correct_spreadsheet:str):
    #     self._original_spreadsheet = original_spreadsheet.replace('"', '')
    #     self._to_correct_spreadsheet = original_spreadsheet.replace('"', '')

    #     try:
    #         self._corrected_df.to_excel(f'CORRECTED_{self._original_spreadsheet_name[:-4]}.xlsx')
    #     except Exception as e:
    #         print('Error to update original spreadsheet: ', e)
