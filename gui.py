import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from image_editor import *
from scraper import parse_game_info
from settings import SettingsWindow
from calculator import CalculatorWindow


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PS Store Reseller App")
        self.geometry("500x650")

        # Создаем поля для ввода
        self.create_label_entry("Ссылка:", "game_link")  # Добавляем новое поле для ввода ссылки

        # Создаем кнопку для парсинга
        parse_button = ttk.Button(self, text="Парсить", command=self.parse)  # Добавляем новую кнопку для парсинга
        parse_button.pack(pady=10)

        self.create_label_entry("Название:", "game_name")
        self.create_label_combobox("Русский язык:", "russian_language",
                                   ["РУССКИЕ СУБТИТРЫ", "ПОЛНОСТЬЮ НА РУССКОМ", "АНГЛИЙСКИЙ ЯЗЫК"])
        self.create_label_combobox("Платформы:", "platforms", ["Xbox ONE", "Xbox Series X", "Xbox Series S", "One,Series S|X"])
        self.create_label_combobox("Версия игры:", "game_version", ["Standard Edition", "Deluxe Edition"])
        self.create_label_entry("Цена:", "game_price")
        self.create_label_entry("Скидка:", "discount")
        self.create_label_entry("Дата окончания скидки:", "discount_end_date")

        # Создаем кнопку для выбора изображения
        self.image_path = tk.StringVar()
        choose_image_button = ttk.Button(self, text="Выбрать изображение", command=self.choose_image)
        choose_image_button.pack(pady=10)

        # Создаем кнопку отправить
        submit_button = ttk.Button(self, text="Отправить", command=self.submit)
        submit_button.pack(pady=10)

        # Добавляем кнопку "Настройки"
        settings_button = tk.Button(self, text="Настройки", command=self.open_settings)
        settings_button.pack(pady=10)

        # Добавляем кнопку "Калькулятор"
        calculator_button = tk.Button(self, text="Калькулятор", command=self.open_calculator)
        calculator_button.pack(pady=10)

    def open_settings(self):
        # Создаем новое окно настроек
        settings_window = SettingsWindow(self)

    def open_calculator(self):
        # Создаем новое окно калькулятор
        calculator_window = CalculatorWindow(self)

    def parse(self):
        # Получаем ссылку из поля для ввода
        game_link = self.game_link.get()

        # Парсим информацию с сайта
        game_name, platforms, price, discount, language, discount_end_date = parse_game_info(game_link)

        # Заполняем поля для ввода
        self.game_name.set(game_name)
        self.platforms.set(platforms)
        self.game_price.set(price)
        self.discount.set(discount)  # Устанавливаем значение поля "Скидка"
        self.russian_language.set(language)
        self.discount_end_date.set(discount_end_date)  # Добавьте эту строку

    def create_label_entry(self, label_text, entry_var_name):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем поле для ввода
        entry_var = tk.StringVar()
        setattr(self, entry_var_name, entry_var)
        entry = ttk.Entry(self, textvariable=entry_var)
        entry.pack(fill='x', padx=5)

    def create_label_combobox(self, label_text, combobox_var_name, values):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем выпадающий список
        combobox_var = tk.StringVar()
        setattr(self, combobox_var_name, combobox_var)
        combobox = ttk.Combobox(self, textvariable=combobox_var, values=values)
        combobox.pack(fill='x', padx=5)

    def choose_image(self):
        # Открываем диалог выбора файла и сохраняем путь к выбранному файлу
        file_path = filedialog.askopenfilename()
        self.image_path.set(file_path)

    def submit(self):
        # Получаем данные из полей для ввода
        game_link = self.game_link.get()
        game_name = self.game_name.get()
        russian_language = self.russian_language.get()
        platforms = self.platforms.get()

        game_version = self.game_version.get()
        game_price = self.game_price.get()
        discount = self.discount.get()
        discount_end_date = self.discount_end_date.get()

        discount_position_square = [3000, 3620]
        discount_position_text = [3030, 3810]

        if discount:
            editor = ImageEditor("newtemplate.png")
            price_position = [705, 3600]
        else:
            # Создаем экземпляр ImageEditor и добавляем текст на изображение
            editor = ImageEditor("newtemplate2.png")
            price_position = [705, 3500]

        editor.add_text(game_name, (700, 3250), "fonts/Segoe UI.ttf", 150, "black")

        # Используем функцию add_gradient_text для добавления цены с градиентом
        editor.add_gradient_text(game_price, price_position, "fonts/Segoe UI Bold.ttf", 600)

        editor.add_text(russian_language, (1320, 3100), "fonts/Segoe UI Bold.ttf", 85, "white")
        editor.add_text(platforms, (750, 3090), "fonts/Segoe UI Bold.ttf", 110, "white")
        editor.add_text(game_version, (705, 3430), "fonts/Segoe UI Bold.ttf", 130, "gray")

        if len(game_price) >= 6:
            pass
        else:
            discount_position_square[0] -= 250
            discount_position_text[0] -= 250

        # # Определяем регион игры и загружаем соответствующее изображение
        # if "ua-store" in game_link:
        #     region_image = Image.open("ukraine.png")
        # elif "tr-store" in game_link:
        #     region_image = Image.open("turkey.png")
        #
        # # Изменяем размер изображения, сохраняя пропорции
        # max_size = (838, 838)
        # region_image.thumbnail(max_size)

        # Добавляем изображение региона на итоговое изображение
        # editor.image.paste(region_image, (2570, 3071), region_image)

        # Load the discount square image
        discount_square = Image.open("square.png")

        # Resize the discount square image (replace 'new_width' and 'new_height' with your desired size)
        discount_square = discount_square.resize((650, 650))

        # Open the background image
        background = Image.open(self.image_path.get())

        # Изменяем размер фонового изображения
        width_ratio = 4096 / background.width
        height_ratio = 3565 / background.height
        ratio = max(width_ratio, height_ratio)
        new_width = int(background.width * ratio)
        new_height = int(background.height * ratio)
        background = background.resize((new_width, new_height))

        # Обрезаем фоновое изображение
        left_margin = (background.width - 4096) / 2
        top_margin = (background.height - 3565) / 2
        background = background.crop((left_margin, top_margin, left_margin + 4096, top_margin + 3565))

        # Создаем черное изображение нужного размера
        black_square = Image.new('RGB', (4096, 4857 - 3565), color='black')

        # Объединяем фоновое изображение и черный квадрат
        final_image = Image.new('RGB', (4096, 4857))
        final_image.paste(background, (0, 0))
        final_image.paste(black_square, (0, 3565))

        # Paste the discount square onto the image (replace 'x' and 'y' with your desired coordinates)
        if discount:
            editor.image.paste(discount_square, discount_position_square, discount_square)
            editor.add_text(discount, discount_position_text, "fonts/Segoe UI.ttf", 220, "white")
            editor.add_text(discount_end_date, (1200, 4300), "fonts/Segoe UI Bold.ttf", 100, "gray")

        # Накладываем шаблон на фоновое изображение
        final_image.paste(editor.image.resize((4096, 4857)), (0, 0), editor.image.resize((4096, 4857)))

        # Сохраняем изображение с уникальным именем файла
        output_path = "output/output.png"
        i = 1
        while os.path.exists(output_path):
            output_path = f"output/output{i}.png"
            i += 1

        final_image.save(output_path)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
