import pandas as pd

def read_two_columns_excel(column1, column2, spreadsheet):
    df = pd.read_excel(spreadsheet)

    return (df[column1] + ' ' + df[column2]).values

for i in read_two_columns_excel('Genus1', 'Species1', 'Lepidoptera_-_Importacao_IX_lote_1.xls'):
    print(i)
