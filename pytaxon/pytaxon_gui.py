import customtkinter as ctk
from tkinter import Tk, filedialog, ttk, Toplevel, Entry, Button
from PIL import Image, ImageTk
import subprocess
from CTkMessagebox import CTkMessagebox
from openpyxl import load_workbook

def open_file(entry_widget):
    filetypes = [("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, filepath)

def run_pytaxon(input_path, source_id, check_spreadsheet_name):
    columns = "species,genus,family,order,class,phylum,kingdom,scientificName"
    command = ["python", "main.py", "-i", input_path, "-r", columns, "-c", check_spreadsheet_name, "-si", source_id]
    try:
        subprocess.run(command, check=True)
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

        load_data_in_treeview(tree, headers, data)

        if spreadsheet_name:
            load_spreadsheet_additional(f"{spreadsheet_name}.xlsx", tree2)
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Erro ao carregar a planilha: {e}", icon="cancel")

def load_spreadsheet_additional(file_path, treeview):
    workbook_spreadsheet = load_workbook(filename=file_path, data_only=False)
    sheet_spreadsheet = workbook_spreadsheet.active

    treeview['columns'] = [sheet_spreadsheet.cell(row=1, column=col).value for col in range(1, sheet_spreadsheet.max_column + 1)]
    treeview['show'] = 'headings'

    for col in treeview['columns']:
        treeview.heading(col, text=col)
        treeview.column(col, width=100, anchor='center')

    for row in range(2, sheet_spreadsheet.max_row + 1):
        values = [sheet_spreadsheet.cell(row=row, column=col).value for col in range(1, sheet_spreadsheet.max_column + 1)]
        treeview.insert('', 'end', values=values)

    treeview.bind('<Double-1>', lambda event: on_double_click(event, treeview, sheet_spreadsheet, file_path))

def on_double_click(event, treeview, sheet, filepath):
    item = treeview.selection()[0]
    col = int(treeview.identify_column(event.x)[1:])
    row = treeview.index(item) + 2

    value = treeview.item(item, 'values')[col - 1]

    popup = Toplevel()
    popup.geometry("200x100+680+400")
    entry = Entry(popup)
    entry.insert(0, value)
    entry.pack()
    entry.focus_set()

    def save_new_value():
        new_value = entry.get()
        treeview.item(item, values=update_cell(sheet, row, col, new_value, item, treeview))
        workbook = load_workbook(filename=filepath, data_only=False)
        workbook.active.cell(row=row, column=col, value=new_value)
        workbook.save(filepath)
        popup.destroy()

    button = Button(popup, text="Save", command=save_new_value)
    button.pack()

def update_cell(sheet, row, col, new_value, item, treeview):
    values = list(treeview.item(item, 'values'))
    values[col - 1] = new_value
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
    global tree, tree2
    root = Tk()
    root.title("Pytaxon: a tool for detection and correction of taxonomic data error")
    root.geometry("1400x700")
    root.configure(bg='#002F3E')

    logo_image = Image.open("PyTaxon.png")
    logo_photoimage = ImageTk.PhotoImage(logo_image.resize((250, 250), Image.Resampling.LANCZOS))
    logo_label = ctk.CTkLabel(master=root, image=logo_photoimage)
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
    tree = ttk.Treeview(frame3)
    tree.place(relx=0.055, rely=0.1, relwidth=0.9, relheight=0.7)

    frame4 = ctk.CTkFrame(master=root, corner_radius=10, fg_color=frame_color)
    frame4.place(relx=0.62, rely=0.44, relwidth=0.36, relheight=0.51)
    tree2 = ttk.Treeview(frame4)
    tree2.place(relx=0.055, rely=0.1, relwidth=0.9, relheight=0.7)

    root.mainloop()


create_layout()



