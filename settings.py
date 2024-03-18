import tkinter as tk
import os
import json

# Определите ваши начальные коэффициенты здесь
initial_coefficients = {
    "less100tr": 5,
    "less699tr": 4.6,
    "less1199tr": 4.3,
    "less1799tr": 4.1,
    "more1799tr": 4,
    "percenttr": 0.07,
    "less300ua": 3.2,
    "less1499ua": 3,
    "less1999ua": 2.85,
    "more1999ua": 2.7,
    "percentua": 0.09
}

def load_coefficients(region):
    filename = f"coefficients{region}.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            coefficients = json.load(file)
    else:
        coefficients = initial_coefficients
        save_coefficients(coefficients, region)
    return coefficients

def save_coefficients(coefficients, region):
    filename = f"coefficients{region}.json"
    with open(filename, "w") as file:
        json.dump(coefficients, file)

class SettingsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # Добавляем кнопки для выбора региона
        ua_button = tk.Button(self, text="Украинский регион", command=lambda: self.open_coefficients_window("ua"))
        tr_button = tk.Button(self, text="Турецкий регион", command=lambda: self.open_coefficients_window("tr"))

        ua_button.pack(pady=10)
        tr_button.pack(pady=10)

    def open_coefficients_window(self, region):
        # Загружаем коэффициенты
        self.coefficients = load_coefficients(region)

        # Создаем новое окно
        coefficients_window = tk.Toplevel(self)

        # Добавляем поля для ввода коэффициентов
        entries = {}
        if region == "tr":
            for price in ["100", "699", "1199", "1799"]:
                label = tk.Label(coefficients_window, text=f"Коэффициент для игр дешевле {price}:")
                entry = tk.Entry(coefficients_window)
                # Вставляем текущее значение коэффициента в поле для ввода
                entry.insert(0, self.coefficients[f"less{price}{region}"])
                label.pack()
                entry.pack()
                entries[f"less{price}{region}"] = entry

            label = tk.Label(coefficients_window, text=f"Коэффициент для игр дороже 1799:")
            entry = tk.Entry(coefficients_window)
            # Вставляем текущее значение коэффициента в поле для ввода
            entry.insert(0, self.coefficients[f"more1799{region}"])
            label.pack()
            entry.pack()
            entries[f"more1799{region}"] = entry
        elif region == "ua":
            for price in ["300", "1499", "1999"]:
                label = tk.Label(coefficients_window, text=f"Коэффициент для игр дешевле {price}:")
                entry = tk.Entry(coefficients_window)
                # Вставляем текущее значение коэффициента в поле для ввода
                entry.insert(0, self.coefficients[f"less{price}{region}"])
                label.pack()
                entry.pack()
                entries[f"less{price}{region}"] = entry

            label = tk.Label(coefficients_window, text=f"Коэффициент для игр дороже 1999:")
            entry = tk.Entry(coefficients_window)
            # Вставляем текущее значение коэффициента в поле для ввода
            entry.insert(0, self.coefficients[f"more1999{region}"])
            label.pack()
            entry.pack()
            entries[f"more1999{region}"] = entry

        # Добавляем поле для ввода процента
        label = tk.Label(coefficients_window, text="Процент:")
        entry = tk.Entry(coefficients_window)
        # Вставляем текущее значение процента в поле для ввода
        entry.insert(0, self.coefficients[f"percent{region}"])
        label.pack()
        entry.pack()
        entries[f"percent{region}"] = entry

        # Добавляем кнопку для сохранения коэффициентов
        save_button = tk.Button(coefficients_window, text="Сохранить",
                                command=lambda: save_coefficients({k: float(v.get()) for k, v in entries.items()},
                                                                  region))
        save_button.pack(pady=10)




