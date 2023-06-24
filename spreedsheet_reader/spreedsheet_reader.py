import pandas as pd

def read_two_columns_excel(spreadsheet, column1, column2=False) -> list:
    df = pd.read_excel(spreadsheet).reset_index()

    if column2:
        return list([df['index'], (df[column1] + ' ' + df[column2]).values])
    else:
        return list(df[column1].values)

print(list(read_two_columns_excel('db/Lepidoptera_-_Importacao_IX_lote_1.xls', 'Genus1', 'Species1')))
