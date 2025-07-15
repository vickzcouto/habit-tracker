import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
from pathlib import Path

HABITS = [
    "oração da manhã",
    "meditação",
    "alongamento",
    "exercício físico",
    "caminhada",
    "estudos python",
    "estudos infra",
    "leitura diária",
    "desenho",
    "aprendi algo novo",
    "gratidão/afirmações",
    "oração noturna",
]

DATA_FILE = "habit_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    # Ordena as datas em ordem crescente (mais antiga em cima, mais recente embaixo)
    data = dict(sorted(data.items(), key=lambda x: datetime.strptime(x[0], "%d-%m-%Y") if '-' in x[0] and x[0].count('-')==2 and len(x[0].split('-')[2])==4 else datetime.strptime(x[0], "%Y-%m-%d")))
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def format_date(date_obj):
    return date_obj.strftime("%d-%m-%Y")

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")

        self.data = load_data()

        tk.Label(root, text="Selecione a data:").pack()
        self.date_picker = DateEntry(root, width=12, background='pink',
                                     foreground='black', borderwidth=2, date_pattern='y-mm-dd')
        self.date_picker.pack(pady=5)
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_change)

        self.checkbox_frame = tk.Frame(root)
        self.checkbox_frame.pack()

        self.vars = {}
        self.current_day = format_date(self.date_picker.get_date())
        self.build_checkboxes()

        tk.Button(root, text="Salvar Progresso", command=self.save_progress).pack(pady=5)
        tk.Button(root, text="Sair", command=root.quit).pack()

        #Teste de logo
        self.root = root
        self.root.geometry("800x600")
        img_path = Path("img/logo.png")
        pil_image = Image.open(img_path).resize((60, 30), Image.LANCZOS)
        tkinter_image = ImageTk.PhotoImage(pil_image)
        logo_label = tk.Label(root, image=tkinter_image, bg='white')
        logo_label.image = tkinter_image
        logo_label.place(relx=1.0, x=-10, y=10, anchor='ne')
        #fim

    def build_checkboxes(self):
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        if self.current_day not in self.data:
            self.data[self.current_day] = {habit: False for habit in HABITS}

        self.vars.clear()
        for habit in HABITS:
            var = tk.BooleanVar(value=self.data[self.current_day].get(habit, False))
            cb = tk.Checkbutton(self.checkbox_frame, text=habit, variable=var)
            cb.pack(anchor='w')
            self.vars[habit] = var

    def on_date_change(self, event):
        self.current_day = format_date(self.date_picker.get_date())
        self.build_checkboxes()

    def save_progress(self):
        for habit, var in self.vars.items():
            self.data[self.current_day][habit] = var.get()
        save_data(self.data)
        messagebox.showinfo("Salvo", f"Progresso de {self.current_day} salvo com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
