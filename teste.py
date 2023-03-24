from openpyxl import Workbook

mano = {'oi': [0, 1, 2], 'ola': [1]}

wb = Workbook()

# grab the active worksheet
ws = wb.active

# Data can be assigned directly to cells
# ws['A1'] = 42

# Rows can also be appended
ws.append([1, 2, 3])
ws.append([1, 2, 3])
# Save the file
wb.save("sample.xlsx")