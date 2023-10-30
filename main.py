from pytaxon import Pytaxon

if __name__ == '__main__':
    pt = Pytaxon()
    print(pt.logo)
    # pt.read_spreadshet(input('Digite o caminho do seu arquivo: '))
    pt.read_spreadshet("F:/0 - Bibliotecas Windows/Área de trabalho/pytaxon/pytaxon-cli/Lepidoptera_-_Importacao_IX_lote_1.xls")

    while True:
        match input(pt.menu):
            case '1':
                # pt.read_taxon_columns(*input('Digite o nome das colunas do Genero e da Especie: ').split())
                pt.read_taxon_columns(*['Genus1', 'Species1'])
                pt.connect_to_api_taxony()
                pt.data_incorrect_taxons()
                pt.create_taxonomies_pivot_spreadsheet()

            case '2':
                pt.update_original_spreadsheet()

            case '3':
                # pt.read_lineage_columns(*input('Digite o nome das colunas da Tribo, Família, Ordem, Classe e Filo: ').split())
                pt.read_lineage_columns(*['Tribe1', 'Family', 'Order', 'Class', 'Phylum'])
                pt.connect_to_api_lineage()

            case '4':
                pass

            case _:
                break
