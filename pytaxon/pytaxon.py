import os
import time
from collections import defaultdict
from pathlib import Path

import pandas as pd
from tqdm import tqdm
import requests


class Pytaxon:
    def __init__(self, source_id=None):
        self._source_id:int = int(source_id)

        self._original_df:pd.DataFrame = None

        self.column_vars:list = None
        
        self._incorrect_data:defaultdict = defaultdict(list)

        print(self.logo)
        self.connect_to_api()

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

    def connect_to_api(self) -> None: 
        """
        """    
        if requests.get("http://resolver.globalnames.org/name_resolvers.json").status_code != 200:
            print(f"Could not connect to GNR api")
            exit()
        else:
            print(f"Connected to GNR api")
        time.sleep(1)

    def read_spreadshet(self, original_spreadsheet: str) -> pd.DataFrame:
        """
        """
        original_spreadsheet_path = original_spreadsheet.replace('"', '')
        original_spreadsheet = os.path.basename(original_spreadsheet_path)
        original_spreadsheet_name, _ = os.path.splitext(original_spreadsheet)

        self._original_df = pd.read_excel(original_spreadsheet_path).fillna('')

        print(f'Spreadsheet {original_spreadsheet_name} read.')
        time.sleep(1)

        return self._original_df
    
    def read_columns(self, column_vars:list) -> None:
        """
        """
        self.column_vars = [column.strip() for column in column_vars.split(',')]

        missing_columns = [column for column in self.column_vars if column not in self._original_df.columns]

        if not missing_columns:
            print('Columns choosed.')
        else:
            print(f"The following columns were not found: {', '.join(missing_columns)}")
            exit()

    def compare_data(self, line, column_error, wrong_data, corrected_data=None, id_number=None) -> tuple:
        """
        """
        def choose_id():
            id_links = {
                1: ('COL ID Source', f'=HYPERLINK("https://www.checklistbank.org/dataset/278910/taxon/{id_number}", "{id_number}")'),
                4: ('NCBI ID Source', f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={id_number}", "{id_number}")'), 
                11: ('GBIF ID Source', f'=HYPERLINK("https://www.gbif.org/species/{id_number}", "{id_number}")'),
                180: ('INAT ID Source', f'=HYPERLINK("https://www.inaturalist.org/taxa/{id_number}, {id_number}")')
            }

            return id_links[self._source_id][0], id_links[self._source_id][1]

        self._id_column_name, id_hyperlink = choose_id()

        try:
            if self.ignore_incertae_sedis and wrong_data == 'incertae sedis':
                pass
            elif corrected_data != wrong_data:
                self._incorrect_data['Error Line'].append(line)
                self._incorrect_data['Rank'].append(column_error)
                self._incorrect_data['Wrong Name'].append(wrong_data)
                self._incorrect_data['Suggested Name'].append(corrected_data)
                self._incorrect_data[self._id_column_name].append(id_hyperlink)
                self._incorrect_data['Change'].append('y/n')
        except:
            self._incorrect_data['Error Line'].append(line)
            self._incorrect_data['Rank'].append(column_error)
            self._incorrect_data['Wrong Name'].append(wrong_data)
            self._incorrect_data['Suggested Name'].append('No Correspondence')
            self._incorrect_data[self._id_column_name].append('No ID')
            self._incorrect_data['Change'].append('No Correspondence')

    def verify_taxon(self, nome_taxon:str) -> dict:
        """
        """
        valid_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
        url = "http://resolver.globalnames.org/name_resolvers.json"
        params = {
            'names': nome_taxon,
            'best_match_only': True,
            'data_source_ids': self._source_id,
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            service = data['data'][0]['results'][0]
            if 'data' in data and data['data']:
                paths = service['classification_path'].split('|')
                ids = service['classification_path_ids'].split('|')
                ranks = service['classification_path_ranks'].split('|')

                result = {}
                for i, rank in enumerate(ranks):
                    if rank in valid_ranks:
                        result[rank] = [paths[i], ids[i] if ids != [''] else 'No ID']
                result['scientificName'] = [service['name_string'], service['taxon_id'] if \
                                            service['taxon_id'] != [''] else 'No ID']
                    
                for rank in valid_ranks:
                    if rank not in result:
                        result[rank] = ['', '']

                return result

    def check_species_and_lineage(self, ignore_incertae_sedis:bool=False) -> None:
        """
        """
        self.ignore_incertae_sedis = ignore_incertae_sedis

        for counter in tqdm(range(len(self._original_df))):
            choosen_taxon = self._original_df[self.column_vars[-1]][counter]
            if not choosen_taxon:
                self.compare_data(counter+2, self.column_vars[0], self._original_df[self.column_vars[0]][counter])
                continue
            try:
                lineage = self.verify_taxon(choosen_taxon)
            except:
                self.compare_data(counter+2, 'Data Incomplete', choosen_taxon)
                continue
            
            if not lineage:
                self.compare_data(counter+2, 'Taxon Not Found', choosen_taxon)
                continue
            
            self.compare_data(counter+2, self.column_vars[0], self._original_df[self.column_vars[0]][counter], 
                              lineage['kingdom'][0], lineage['kingdom'][1])
            self.compare_data(counter+2, self.column_vars[1], self._original_df[self.column_vars[1]][counter], 
                              lineage['phylum'][0], lineage['phylum'][1])
            self.compare_data(counter+2, self.column_vars[2], self._original_df[self.column_vars[2]][counter], 
                              lineage['class'][0], lineage['class'][1])
            self.compare_data(counter+2, self.column_vars[3], self._original_df[self.column_vars[3]][counter], 
                              lineage['order'][0], lineage['order'][1])
            self.compare_data(counter+2, self.column_vars[4], self._original_df[self.column_vars[4]][counter], 
                              lineage['family'][0], lineage['family'][1])
            self.compare_data(counter+2, self.column_vars[5], self._original_df[self.column_vars[5]][counter], 
                              lineage['genus'][0], lineage['genus'][1])
            self.compare_data(counter+2, self.column_vars[6], self._original_df[self.column_vars[6]][counter], 
                              lineage['species'][0], lineage['species'][1])
            self.compare_data(counter+2, self.column_vars[7], self._original_df[self.column_vars[7]][counter], 
                              lineage['scientificName'][0], lineage['scientificName'][1])
            
    def return_output_dir(self):
        """
        Cria, caso não exista, senão retorna o path da pasta Pytaxon-Output de cada sistema operacional
        """
        if os.name == 'nt':  # Windows
            self.pasta_home = Path.home()
        elif os.name == 'posix':  # Linux or macOS
            self.pasta_home = Path.home()
        else:
            self.pasta_home = None
            print("Sistema operacional não suportado.")

        pytaxon_output_dir = self.pasta_home / 'Pytaxon-Output'
        pytaxon_output_dir.mkdir(exist_ok=True)
        return pytaxon_output_dir

    def create_to_correct_spreadsheet(self, spreadsheet_name:str) -> None:
        """
        Cria a planilha de sugestão de correção
        """       
        if self._incorrect_data:
            to_correct_df = pd.DataFrame(self._incorrect_data).style.map(
                lambda x: 'color: blue; text-decoration: underline;',
                subset=self._id_column_name,
            )

            to_correct_spreadsheet_path = self.return_output_dir() / f'{spreadsheet_name}.xlsx'
            print('File created at: ', to_correct_spreadsheet_path)
            to_correct_df.to_excel(to_correct_spreadsheet_path)
            return to_correct_spreadsheet_path
        else:
            log_message = 'No errors in spreadsheet'
            print(log_message)
            with open("spreadsheet_log.txt", "a") as log_file:
                log_file.write(f"{log_message}\n")
            print('log_message')

    def update_original_spreadsheet(self, original_spreadsheet:str, to_correct_spreadsheet:str, spreadsheet_name:str) -> None:
        """
        """
        original_data_df = self.read_spreadshet(original_spreadsheet)
        to_correct_df = self.read_spreadshet(to_correct_spreadsheet)

        for index, row in to_correct_df.iterrows():
            if row['Change'] == 'y':
                original_data_df.at[row['Error Line']-2, row['Rank']] = row['Suggested Name']
        
        corrected_spreadsheet = original_data_df.copy()

        try:
            corrected_spreadsheet_path = self.return_output_dir() / f'{spreadsheet_name}.xlsx'
            print('File created at: ', corrected_spreadsheet_path)
            corrected_spreadsheet.to_excel(corrected_spreadsheet_path, index=False)
            return corrected_spreadsheet_path
        except Exception as e:
            print('Error to update original spreadsheet: ', e)
