import os

import customtkinter as ctk
from tkinter import Tk, filedialog, ttk, Toplevel, Entry, Button
from PIL import Image, ImageTk
import subprocess
from CTkMessagebox import CTkMessagebox
from openpyxl import load_workbook

from tkinter import Label


def open_file(entry_widget):
    filetypes = [("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, filepath)


def run_pytaxon_correct(input_entry, spreadsheet_name_entry, corrected_spreadsheet_entry):
    input_path = input_entry.get()
    check_spreadsheet_name = f"{spreadsheet_name_entry.get()}.xlsx"
    output_path = corrected_spreadsheet_entry.get()

    # Configura os argumentos do comando de forma similar à função run_pytaxon
    command = ["pytaxon", "-os", input_path, "-cs", check_spreadsheet_name, "-o", output_path]

    try:
        subprocess.run(command, check=True)
        CTkMessagebox(message="Pytaxon correction has been run successfully.", icon="check", option_1="Ok")
        clear_treeviews()  # Limpa as visualizações após a execução bem-sucedida

        # Limpa o campo corrected_spreadsheet_entry após a execução bem-sucedida
        corrected_spreadsheet_entry.delete(0, ctk.END)

    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Error", message=f"An error occurred while running Pytaxon correction: {e}", icon="cancel")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An unexpected error occurred: {e}", icon="cancel")

# Adicione esta nova função para limpar os Treeviews
def clear_treeviews():
    global tree, tree2
    for item in tree.get_children():
        tree.delete(item)
    for item in tree2.get_children():
        tree2.delete(item)
    tree['columns'] = []
    tree2['columns'] = []

def run_pytaxon(input_path, source_id, check_spreadsheet_name):
    columns = "species,genus,family,order,class,phylum,kingdom,scientificName"
    command = ["pytaxon", "-i", input_path, "-r", columns, "-c", check_spreadsheet_name, "-si", source_id]
    try:
        subprocess.run(command, check=True)

        log_file_path = "spreadsheet_log.txt"

        # Verificar se o arquivo de log existe e contém a mensagem específica
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                content = file.read().strip()
                if content == 'No errors in spreadsheet':
                    CTkMessagebox(message="No errors in spreadsheet.", icon="check", option_1="Ok")
                    os.remove(log_file_path)  # Apagar o arquivo de log
                    clear_treeviews()
                    return

        CTkMessagebox(message="Pytaxon has been run successfully.", icon="check", option_1="Ok")
        load_spreadsheet(input_path, check_spreadsheet_name)
    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Error", message=f"An error occurred while running Pytaxon: {e}", icon="cancel")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An unexpected error occurred: {e}", icon="cancel")

def show_id_info():
    CTkMessagebox(message="IDs Data Sources:\n"
                          "1 - Catalogue of Life Checklist\n"
                          "4 - NBCI\n"
                          "11 - GBIF\n"
                          "180 - iNaturalist Taxonomy", option_1="Ok")

def load_spreadsheet(file_path, spreadsheet_name=""):
    try:
        workbook = load_workbook(filename=file_path, data_only=True)
        sheet = workbook.active
        headers = ["Line"] + [cell.value for cell in sheet[1] if cell.value in
                              ["species", "genus", "family", "order", "class", "phylum", "kingdom", "scientificName"]]
        data = [[idx + 2] + [row[idx].value for idx, cell in enumerate(sheet[1]) if cell.value in headers[1:]]
                for idx, row in enumerate(sheet.iter_rows(min_row=2))]

        # Aqui você deve ter previamente definido a variável global 'tree'
        load_data_in_treeview(tree, headers, data)

        if spreadsheet_name:
            # Aqui você deve ter previamente definido a variável global 'tree2'
            load_spreadsheet_additional(f"{spreadsheet_name}.xlsx", tree2)
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Erro ao carregar a planilha: {e}", icon="cancel")

    return sheet, file_path  # Retornando a sheet ativa e o caminho do arquivo


def load_spreadsheet_additional(file_path, treeview):
    workbook_spreadsheet = load_workbook(filename=file_path, data_only=False)
    sheet_spreadsheet = workbook_spreadsheet.active
    treeview['columns'] = [sheet_spreadsheet.cell(row=1, column=col).value for col in range(2, sheet_spreadsheet.max_column + 1)]
    treeview['show'] = 'headings'  # Para não mostrar a coluna de índices padrão do treeview

    # Configura o cabeçalho e a largura das colunas no treeview.
    for col in treeview['columns']:
        treeview.heading(col, text=col)
        treeview.column(col, width=100, anchor='center')

    # Insere os dados nas colunas do treeview, excluindo os valores da primeira coluna ("None").
    for row in range(2, sheet_spreadsheet.max_row + 1):
        values = [sheet_spreadsheet.cell(row=row, column=col).value for col in range(2, sheet_spreadsheet.max_column + 1)]
        treeview.insert('', 'end', values=values)

    # Este evento é vinculado para permitir a edição de células com um duplo clique.
    # Note que on_double_click é definido para receber três argumentos: evento, treeview e filepath.
    treeview.bind('<Double-1>', lambda event: on_double_click(event, treeview, file_path))



def on_double_click(event, treeview, filepath):
    col_id = treeview.identify_column(event.x)
    col_name = treeview.heading(col_id, 'text')

    if col_name != 'Change':
        print("Apenas a coluna 'Change' pode ser editada.")
        return

    item = treeview.selection()[0]
    row_index = treeview.index(item) + 2  # As linhas no Excel começam em 1, mas precisamos considerar o cabeçalho
    current_value = treeview.item(item, 'values')[treeview['columns'].index(col_name)]

    popup = Toplevel()
    popup.geometry("200x100+690+400")
    entry = Entry(popup)
    entry.insert(0, current_value)
    entry.pack()
    entry.focus_set()

    def save_new_value(entry, row_index, col_name, item, treeview, filepath):
        new_value = entry.get()

        workbook = load_workbook(filename=filepath)
        worksheet = workbook.active  # Assume que a planilha ativa é a correta

        col_letter = None
        for cell in worksheet[1]:  # Procura pelo cabeçalho correto para encontrar a letra da coluna
            if cell.value == col_name:
                col_letter = cell.column_letter
                cell_ref = f"{col_letter}{row_index}"
                worksheet[cell_ref].value = new_value
                print(f"Valor '{new_value}' salvo na célula '{cell_ref}'")
                break
        else:
            print(f"Não foi possível encontrar a coluna '{col_name}' na planilha.")
            return

        workbook.save(filepath)
        workbook.close()
        treeview.set(item, column=col_name, value=new_value)
        print("Treeview atualizado.")
        popup.destroy()

    button = Button(popup, text="Save", command=lambda: save_new_value(
        entry, row_index, col_name, item, treeview, filepath))
    button.pack()




def update_cell(sheet, row, col, new_value, item, treeview):
    # Obtém a lista atual de valores da linha selecionada no treeview
    values = list(treeview.item(item, 'values'))

    # Atualiza o valor na coluna específica
    values[col - 1] = new_value  # col - 1 porque os índices de colunas começam em 1 no treeview, mas em 0 nas listas

    # Retorna a lista de valores atualizados
    return values


def load_data_in_treeview(treeview, headers, data):
    treeview['columns'] = headers
    treeview['show'] = 'headings'

    for header in headers:
        treeview.heading(header, text=header)
        treeview.column(header, width=120)

    for row in treeview.get_children():
        treeview.delete(row)

    for row_data in data:
        treeview.insert("", 'end', values=row_data)


def create_layout():
    global tree, tree2, entry_input, entry_spreadsheet_name, corrected_spreadsheet_entry

    root = Tk()
    root.title("Pytaxon: a tool for detection and correction of taxonomic data error")
    root.geometry("1400x700")
    root.configure(bg='#002F3E')

    logo_image = Image.open("PyTaxon.png")
    logo_photoimage = ImageTk.PhotoImage(logo_image.resize((250, 250), Image.Resampling.LANCZOS))
    logo_label = Label(master=root, image=logo_photoimage)
    logo_label.image = logo_photoimage
    logo_label.place(relx=0.015, rely=0.05)

    frame_color = '#00546D'
    frame1 = ctk.CTkFrame(master=root, corner_radius=10, fg_color=frame_color)
    frame1.place(relx=0.015, rely=0.44, relwidth=0.23, relheight=0.51)

    label_input = ctk.CTkLabel(master=frame1, text="Input spreadsheet", fg_color=frame_color, text_color='white')
    label_input.place(relx=0.05, rely=0.1)
    entry_input = ctk.CTkEntry(master=frame1, placeholder_text="Search for your spreadsheet", fg_color="white")
    entry_input.place(relx=0.05, rely=0.2, relwidth=0.65)
    button_search = ctk.CTkButton(master=frame1, text="Search", fg_color="#004C70", hover_color="#0073A0",
                                  command=lambda: open_file(entry_input))
    button_search.place(relx=0.73, rely=0.2, relwidth=0.22)

    label_columns = ctk.CTkLabel(master=frame1, text="Column Names", fg_color=frame_color, text_color='white')
    label_columns.place(relx=0.05, rely=0.3)
    entry_columns = ctk.CTkEntry(master=frame1,
                                 placeholder_text="Species, Genus, Family, Order, Class, Phylum, Kingdom, ScientificName",
                                 fg_color="white")
    entry_columns.place(relx=0.05, rely=0.4, relwidth=0.9)

    label_source_id = ctk.CTkLabel(master=frame1, text="Source ID", fg_color=frame_color, text_color='white')
    label_source_id.place(relx=0.05, rely=0.5)
    option_menu_source_id = ctk.CTkOptionMenu(master=frame1, values=["1", "4", "11", "180"], fg_color="white")
    option_menu_source_id.place(relx=0.05, rely=0.6, relwidth=0.75)

    button_id_info = ctk.CTkButton(master=frame1, text="ID ?", fg_color="#004C70", hover_color="#0073A0",
                                   command=show_id_info)
    button_id_info.place(relx=0.84, rely=0.59, relwidth=0.12, relheight=0.09)

    label_check_spreadsheet = ctk.CTkLabel(master=frame1, text="Check Spreadsheet Name", fg_color=frame_color,
                                           text_color='white')
    label_check_spreadsheet.place(relx=0.05, rely=0.7)
    entry_spreadsheet_name = ctk.CTkEntry(master=frame1, placeholder_text="Spreadsheet name, no extension",
                                          fg_color="white")
    entry_spreadsheet_name.place(relx=0.05, rely=0.8, relwidth=0.65)
    button_run = ctk.CTkButton(master=frame1, text="Run", fg_color="#004C70", hover_color="#0073A0",
                               command=lambda: run_pytaxon(entry_input.get(), option_menu_source_id.get(),
                                                           entry_spreadsheet_name.get()))
    button_run.place(relx=0.73, rely=0.8, relwidth=0.22)

    frame2 = ctk.CTkFrame(master=root, corner_radius=10, fg_color=frame_color)
    frame2.place(relx=0.25, rely=0.05, relwidth=0.73, relheight=0.38)

    frame3 = ctk.CTkFrame(master=root, corner_radius=10, fg_color=frame_color)
    frame3.place(relx=0.25, rely=0.44, relwidth=0.36, relheight=0.51)
    label_user_spreadsheet = Label(master=root, text="User Spreadsheet", bg=frame_color, fg='white')
    label_user_spreadsheet.place(relx=0.27, rely=0.45)

    tree = ttk.Treeview(frame3)
    tree.place(relx=0.055, rely=0.1, relwidth=0.9, relheight=0.7)

    frame4 = ctk.CTkFrame(master=root, corner_radius=10, fg_color=frame_color)
    frame4.place(relx=0.62, rely=0.44, relwidth=0.36, relheight=0.51)
    label_check_spreadsheet = Label(master=root, text="Check Spreadsheet", bg=frame_color, fg='white')
    label_check_spreadsheet.place(relx=0.64, rely=0.45)

    tree2 = ttk.Treeview(frame4)
    tree2.place(relx=0.055, rely=0.1, relwidth=0.9, relheight=0.7)

    corrected_spreadsheet_label = ctk.CTkLabel(master=frame4, text="Corrected spreadsheet name", fg_color=frame_color,
                                               text_color='white')
    corrected_spreadsheet_label.place(relx=0.055, rely=0.82)

    corrected_spreadsheet_entry = ctk.CTkEntry(master=frame4, fg_color="white")
    corrected_spreadsheet_entry.place(relx=0.45, rely=0.82, relwidth=0.50)

    correct_button = ctk.CTkButton(master=frame4, text="Correct", fg_color="#004C70", hover_color="#0073A0",
                                   command=lambda: run_pytaxon_correct(entry_input, entry_spreadsheet_name,
                                                                       corrected_spreadsheet_entry))
    correct_button.place(relx=0.45, rely=0.90, relwidth=0.50)

    root.mainloop()

create_layout()



