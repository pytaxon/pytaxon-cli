from pytaxon import Pytaxon

menu = '''[1] Analyze TAXONOMIES (species name) and create a pivot
[2] Correct original spreadsheet through pivot
[3] Analyze LINEAGE and create a pivot
[4] Correct original spreadsheet through pivot
Choose a option: '''

if __name__ == '__main__':
    while True:
        match input(menu):
            case '1':
                pt = Pytaxon()
                pt.read_spreadshet(input('Digite o caminho do seu arquivo: '))
                pt.enter_columns_names(input('Digite o nome das colunas do Genero e da Especie: ').split())
                pt.connect_to_api()
                pt.data_incorrect_taxons()
                pt.create_taxonomies_pivot_spreadsheet()
            case '2':
                pt.update_original_spreadsheet()
            case _:
                break
