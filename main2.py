from pytaxon import Pytaxon_GBIF

if __name__ == '__main__':
    pt = Pytaxon_GBIF()
    print(pt.logo)

    if not pt.connect_to_api:
        exit()
    pt.read_spreadshet("F:/0 - Bibliotecas Windows/Área de trabalho/pytaxon/pytaxon-cli/db/Lepidoptera_planilha.xlsx")
    pt.read_columns()
    pt.check_species_and_lineage()
    