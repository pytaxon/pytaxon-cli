
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess

class PytaxonGUI:
    def __init__(self, master):
        self.master = master
        master.title("Pytaxon GUI")
        self.setup_gui()

    def setup_gui(self):
        # Campo de entrada para o arquivo de origem
        tk.Label(self.master, text="Input File:").grid(row=0, column=0)
        self.input_file = tk.Entry(self.master, width=50)
        self.input_file.grid(row=0, column=1)
        tk.Button(self.master, text="Browse", command=self.open_file).grid(row=0, column=2)

        # Campo de entrada para os nomes das colunas
        tk.Label(self.master, text="Column Names:").grid(row=1, column=0)
        self.column_names = tk.Entry(self.master, width=50)
        self.column_names.grid(row=1, column=1)

        # Opções de fonte de dados
        tk.Label(self.master, text="Source ID:").grid(row=2, column=0)
        self.source_id = ttk.Combobox(self.master, values=[1, 4, 11, 180])
        self.source_id.grid(row=2, column=1)

        # Campo de entrada para o nome da planilha de checagem
        tk.Label(self.master, text="Check Spreadsheet Name:").grid(row=3, column=0)
        self.check_spreadsheet_name = tk.Entry(self.master, width=50)
        self.check_spreadsheet_name.grid(row=3, column=1)

        # Botão para executar a verificação
        tk.Button(self.master, text="Run Pytaxon", command=self.run_pytaxon).grid(row=4, column=1)

    def open_file(self):
        filetypes = [("Excel files", "*.xlsx"), ("Old Excel files", "*.xls"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.input_file.delete(0, tk.END)
            self.input_file.insert(0, filepath)

    def run_pytaxon(self):
        input_path = self.input_file.get()
        columns = self.column_names.get()
        source_id = self.source_id.get()
        check_spreadsheet_name = self.check_spreadsheet_name.get()

        # Construir o comando para subprocess.run
        command = ["python", "main.py", "-i", input_path, "-r", columns, "-c", check_spreadsheet_name, "-si", source_id]

        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", f"Pytaxon has been run successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running Pytaxon: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def main():
    root = tk.Tk()
    app = PytaxonGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
