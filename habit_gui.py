import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime

HABITS = [
    "oração da manhã",
    "meditação manhã",
    "alongamento",
    "exercício físico",
    "caminhada",
    "estudos python",
    "estudos infra",
    "leitura diária",
    "desenho",
    "meditação noturna",
    "oração noturna",
]

DATA_FILE = "habit_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    data = dict(sorted(data.items())) 
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
        self.date_picker = DateEntry(root, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.date_picker.pack(pady=5)
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_change)

        self.checkbox_frame = tk.Frame(root)
        self.checkbox_frame.pack()

        self.vars = {}
        self.current_day = format_date(self.date_picker.get_date())
        self.build_checkboxes()

        tk.Button(root, text="Salvar Progresso", command=self.save_progress).pack(pady=5)
        tk.Button(root, text="Sair", command=root.quit).pack()

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
