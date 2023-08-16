from pytaxon import Pytaxon

menu = '''[1] Analyze original spreadsheet and create a pivot
[2] Correct original spreadsheet with pivot
Choose a option: '''

if __name__ == '__main__':
    while True:
        match input(menu):
            case '1':
                pt = Pytaxon(input('Insert the path to your spreadsheet: '))
            case '2':
                pt.update_original_spreadsheet()
            case _:
                break
