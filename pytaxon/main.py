from pytaxon import Pytaxon_OTT

# TODO: choose over services (gbif and opentree)
if __name__ == '__main__':
    pt = Pytaxon_OTT()
    print(pt.logo)
    # pt.read_spreadshet(input('Digite o caminho do seu arquivo: '))
    # pt.read_spreadshet("F:/0 - Bibliotecas Windows/Área de trabalho/pytaxon/pytaxon-cli/db/Opiliones spreadsheet.xlsx")
    pt.read_spreadshet("F:/0 - Bibliotecas Windows/Área de trabalho/pytaxon/pytaxon-cli/db/Lepidoptera_-_Importacao_IX_lote_1.xls")
    pt.read_taxon_columns()
    pt.connect_to_api_taxony()
    pt.data_incorrect_taxons()
    pt.create_taxonomies_pivot_spreadsheet()

    # while True:
    #     match input(pt.menu):
    #         case '1':
    #             # if not pt.connect_to_api:
    #             #     print('Could not connect to OpenTree API')
    #             #     exit()

                

    #         case '2':
    #             pt.update_original_spreadsheet()

    #         case '3':
    #             # pt.read_lineage_columns(*input('Digite o nome das colunas da Tribo, Família, Ordem, Classe e Filo: ').split())
    #             pt.read_lineage_columns(*['Tribe1', 'Family', 'Order', 'Class', 'Phylum'])
    #             pt.connect_to_api_lineage()

    #         case '4':
    #             pass

    #         case _:
    #             break
