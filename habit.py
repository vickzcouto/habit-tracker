import json
import os 
from datetime import datetime 

HABITS = [
    "oração da manha",
    "meditação manha",
    "exercicio em casa",
    "caminhada",
    "estudos python",
    "estudos infra",
    "meditação noturna",
    "oração noturna",
    "leitura diária",
    "desenho"
]

DATA_FILE = "habit_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_today_key():
    return datetime.now().strftime("%Y-%m-%d")

def is_sunday():
    return datetime.now().weekday() == 6  # segunda=0 ... domingo=6

def init_day_data(data, day_key):
    if day_key not in data:
        data[day_key] = {habit: False for habit in HABITS}

def mark_habit_done(data, day_key, habit):
    if habit in HABITS:
        data[day_key][habit] = True

def show_day_status(data, day_key):
    print(f"\nStatus para {day_key}:")
    for habit, done in data[day_key].items():
        status = "✓" if done else "✗"
        print(f"{status} {habit}")

def main():
    if is_sunday():
        print("Domingo é dia livre, sem acompanhamento.")
        return

    data = load_data()
    today = get_today_key()
    init_day_data(data, today)

    while True:
        show_day_status(data, today)
        print("\nDigite o número do hábito para marcar como feito, ou 'q' para sair:")
        for i, habit in enumerate(HABITS, 1):
            print(f"{i}. {habit}")

        choice = input("> ").strip()
        if choice.lower() == 'q':
            break
        if not choice.isdigit():
            print("Entrada inválida.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(HABITS):
            habit = HABITS[idx-1]
            mark_habit_done(data, today, habit)
            save_data(data)
        else:
            print("Número fora do intervalo.")

if __name__ == "__main__":
    main()