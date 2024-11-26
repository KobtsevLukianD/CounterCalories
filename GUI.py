# Графический интерфейс
# В этом файле программируется десктопное приложение с использованием библиотеки tkinter 

import tkinter as tk  # Библиотека для создания интерфейса
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import ProductClasses  # Файл с классами продуктов
from ProductClasses import Product, ProductDatabase, BaseProduct

import memory  # Сохранение базы

import os

# Определяем путь к файлу base.pkl
filename = os.path.join(os.path.dirname(__file__), "base.pkl")

# Попробуем загрузить данные или инициализировать пустую базу данных
loaded_data = memory.file_load(filename)
if loaded_data is None:
    base = ProductDatabase()  # Инициализируем пустую базу
else:
    base = ProductDatabase()
    base.products = loaded_data.get("products", {})
    base.names = loaded_data.get("names", [])

products = []

def product_by_name(name, mass, quantity):
    """На вход поступает строка - название продукта. Функция возвращает объект класса Product, взаимодействуя с Database"""
    for outer_key, inner_dict in base.products.items():  # Пробегаем по всем категориям
        for inner_key, obj in inner_dict.items():  # Пробегаем по всем продуктам данной категории
            if obj.name == name:
                return Product(mass, quantity, name, category=obj.category, kcal=obj.kcal, protein=obj.protein, fat=obj.fat, carbohydrates=obj.carbohydrates)

def centering_in_window(window, width, height):
    """Задаем размер окна и размещаем его по центру экрана"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def calculate_totals(selections, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value):
    """Функция для вычисления сумм калорий, белков, жиров и углеводов"""
    total_kcal = 0
    total_protein = 0
    total_fat = 0
    total_carbohydrates = 0

    for selection in selections:
        for product in selection:
            total_kcal += product.kcal
            total_protein += product.protein
            total_fat += product.fat
            total_carbohydrates += product.carbohydrates

    # Обновляем значения в полях
    kcal_label_value.config(text=f"{total_kcal:.2f} ккал")
    protein_label_value.config(text=f"{total_protein:.2f} г")
    fat_label_value.config(text=f"{total_fat:.2f} г")
    carbohydrates_label_value.config(text=f"{total_carbohydrates:.2f} г")

def update_combobox_values(combobox_diary, products):
    """Функция для обновления всех выпадающих списков"""
    for row in combobox_diary:
        for combobox in row:
            # Обновляем значения выпадающего списка
            combobox["values"] = products

def diary_selection(event, combobox_diary, selections, frame, products, labels, n, m, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value):
    """Обработка выбора в дневнике: обновление списка и пересчет итогов"""
    choice = combobox_diary[n][m].get()
    if str(choice) == " ":
        if len(combobox_diary[n]) > 1 and m != len(combobox_diary[n]) - 1:
            combobox_diary[n][m].pack_forget()
            combobox_diary[n].pop(m)
            selections[n].pop(m)
    else:
        selections[n].append(product_by_name(choice, 100, 1))
        combobox_diary[n][m]["values"] = [" "]
        new_combobox = ttk.Combobox(frame, values=products, state="readonly")
        combobox_diary[n].insert(m + 1, new_combobox)
        new_combobox.pack(anchor=CENTER)
        new_combobox.bind("<<ComboboxSelected>>",
                          lambda event, idx1=n, idx2=m + 1: diary_selection(event, combobox_diary, selections, frame, products, labels, idx1, idx2, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value))

    for i in range(len(combobox_diary)):
        labels[i].pack_forget()
        for j in range(len(combobox_diary[i])):
            combobox_diary[i][j].pack_forget()

    for i in range(len(combobox_diary)):
        labels[i].pack(anchor=CENTER)
        for j in range(len(combobox_diary[i])):
            combobox_diary[i][j].pack(anchor=CENTER)
            combobox_diary[i][j].bind("<<ComboboxSelected>>",
                                      lambda event, idx1=i, idx2=j: diary_selection(event, combobox_diary, selections, frame, products, labels, idx1, idx2, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value))

    calculate_totals(selections, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value)

def AddToDatabase(name_entry, category_entry, protein_entry, fat_entry, carbohydrates_entry, kcal_entry, products, combobox_diary):
    """Добавление нового продукта в базу"""
    name = name_entry.get()
    category = category_entry.get()
    try:
        protein = float(protein_entry.get())
        fat = float(fat_entry.get())
        carbohydrates = float(carbohydrates_entry.get())
        kcal = float(kcal_entry.get())

        if name in base.names:
            messagebox.showerror("Ошибка", "Продукт с таким именем уже существует")
            return
        if protein < 0 or fat < 0 or carbohydrates < 0 or kcal < 0:
            messagebox.showerror("Ошибка", "Нельзя вводить отрицательные значения")
            return

        # Добавляем продукт в базу
        base.add_product(BaseProduct(name, category, kcal, protein, fat, carbohydrates))

        # Обновляем список продуктов
        products.clear()
        products.extend([" "] + base.names)

        # Обновляем выпадающие списки
        update_combobox_values(combobox_diary, products)

        # Очищаем поля ввода
        name_entry.delete(0, END)
        category_entry.delete(0, END)
        protein_entry.delete(0, END)
        fat_entry.delete(0, END)
        carbohydrates_entry.delete(0, END)
        kcal_entry.delete(0, END)

        # Сохраняем базу в файл
        memory.file_save(base, filename)

        # Уведомляем об успешном добавлении
        messagebox.showinfo("Успех", "Продукт успешно добавлен!")

    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовые значения для белков, жиров, углеводов и калорий.")

def clear_database(products, combobox_diary):
    """Очистка базы данных"""
    memory.file_clear(filename)
    base.products.clear()
    base.names.clear()
    products.clear()
    products.append(" ")
    update_combobox_values(combobox_diary, products)

def run_graphics():
    """Основная функция запуска графического интерфейса"""
    num_of_meals = 5
    root = Tk() # Создаем корневой объект
    root.title("Счетчик калорий") # Заголовок
    root_width, root_height = 400, 500 # Ширина и высота окна
    centering_in_window(root, root_width, root_height)
    
    notebook = ttk.Notebook() # Создаем набор вкладок
    notebook.pack(expand = True, fill = BOTH)
    
    diary_frame = ttk.Frame(notebook) # Фрейм с дневным рационом и подсчетом КБЖУ
    diary_frame.pack(expand = True, fill = BOTH)
    base_frame = ttk.Frame(notebook) # Фрейм с базой продуктов
    base_frame.pack(expand = True, fill = BOTH)
    
    # Добавляем фреймы в качестве вкладок
    notebook.add(diary_frame, text = "Дневник")
    notebook.add(base_frame, text = "База")
    
    # Оформление вкладки - дневника питания
    diary_label_d = ttk.Label(diary_frame, text="Дневник питания")
    diary_label_d.pack(anchor=CENTER)
    
    # Список наименований продуктов
    products = [" "] + base.names
    
    # Вспомогательная функция для обновления всех выпадающих списков на diary_frame
    def update_combobox_values(combobox_diary, products):
        for row in combobox_diary:
            for combobox in row:
                # Обновляем только те combobox, где список значений не ограничен (" " не является единственным значением)
                if (combobox["values"] != (" ",) or len(row) < 2):
                    combobox["values"] = products
                    
    selections = [[] for i in range(num_of_meals)]  # Список списков. Во внутреннем списке лежат классы Product
    # Наименование приемов пищи
    diary_labels = [ttk.Label(diary_frame, text="Завтрак"),
                    ttk.Label(diary_frame, text="Обед"),
                    ttk.Label(diary_frame, text="Полдник"),
                    ttk.Label(diary_frame, text="Ужин"),
                    ttk.Label(diary_frame, text="Перекус")]
    
    # Список списков выпадающих меню для разных приемов пищи
    combobox_diary = [[ttk.Combobox(diary_frame, values=products, state="readonly")] for i in range(5)]
    
    # Добавляем поля для отображения сумм
    total_frame = ttk.Frame(diary_frame)
    total_frame.pack(anchor=CENTER, pady=20)

    # Создаем метки и поля для вывода суммарных значений
    kcal_label = ttk.Label(total_frame, text="Калории:")
    kcal_label.grid(row=0, column=0, padx=10, pady=5)
    kcal_label_value = ttk.Label(total_frame, text="0 ккал")
    kcal_label_value.grid(row=0, column=1, padx=10, pady=5)

    protein_label = ttk.Label(total_frame, text="Белки:")
    protein_label.grid(row=0, column=2, padx=10, pady=5)
    protein_label_value = ttk.Label(total_frame, text="0 г")
    protein_label_value.grid(row=0, column=3, padx=10, pady=5)

    fat_label = ttk.Label(total_frame, text="Жиры:")
    fat_label.grid(row=1, column=0, padx=10, pady=5)
    fat_label_value = ttk.Label(total_frame, text="0 г")
    fat_label_value.grid(row=1, column=1, padx=10, pady=5)

    carbohydrates_label = ttk.Label(total_frame, text="Углеводы:")
    carbohydrates_label.grid(row=1, column=2, padx=10, pady=5)
    carbohydrates_label_value = ttk.Label(total_frame, text="0 г")
    carbohydrates_label_value.grid(row=1, column=3, padx=10, pady=5)

    # Вызовем функцию для обновления значений при старте
    calculate_totals(selections, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value)
    
    # Внешний цикл проходит по приемам пищи, внутренний - по всем спискам внутри одного приема пищи
    for i in range(len(combobox_diary)):
        diary_labels[i].pack(anchor=CENTER)
        for j in range(len(combobox_diary[i])):
            combobox_diary[i][j].pack(anchor=CENTER)
            combobox_diary[i][j].bind("<<ComboboxSelected>>", 
                                    lambda event, idx1=i, idx2=j: diary_selection(event, combobox_diary, selections, diary_frame, products, diary_labels, idx1, idx2, kcal_label_value, protein_label_value, fat_label_value, carbohydrates_label_value))

    # Оформление вкладки - базы
    base_label = ttk.Label(base_frame, text="База")
    base_label.pack(anchor=CENTER)

    # Поля ввода для названия и категории продукта
    name_label = ttk.Label(base_frame, text="Название")
    name_label.pack(anchor=W, padx=5)
    name_entry = ttk.Entry(base_frame)
    name_entry.pack(anchor=W, padx=5, fill=X)

    category_label = ttk.Label(base_frame, text="Категория")
    category_label.pack(anchor=W, padx=5)
    category_entry = ttk.Entry(base_frame)
    category_entry.pack(anchor=W, padx=5, fill=X)

    # Поля ввода для белков и жиров на первой строке
    nutrient_frame = ttk.Frame(base_frame)
    nutrient_frame.pack(anchor=W, padx=5, pady=5, fill=X)

    protein_label = ttk.Label(nutrient_frame, text="Белки")
    protein_label.grid(row=0, column=0, padx=5, pady=2)
    protein_entry = ttk.Entry(nutrient_frame, width=10)
    protein_entry.grid(row=0, column=1, padx=5, pady=2)

    fat_label = ttk.Label(nutrient_frame, text="Жиры")
    fat_label.grid(row=0, column=2, padx=5, pady=2)
    fat_entry = ttk.Entry(nutrient_frame, width=10)
    fat_entry.grid(row=0, column=3, padx=5, pady=2)

    # Поля ввода для углеводов и калорий на второй строке
    carbohydrates_label = ttk.Label(nutrient_frame, text="Углеводы")
    carbohydrates_label.grid(row=1, column=0, padx=5, pady=2)
    carbohydrates_entry = ttk.Entry(nutrient_frame, width=10)
    carbohydrates_entry.grid(row=1, column=1, padx=5, pady=2)

    kcal_label = ttk.Label(nutrient_frame, text="Калории")
    kcal_label.grid(row=1, column=2, padx=5, pady=2)
    kcal_entry = ttk.Entry(nutrient_frame, width=10)
    kcal_entry.grid(row=1, column=3, padx=5, pady=2)

    # Кнопка добавления продукта в базу
    add_button = ttk.Button(base_frame, text="Добавить продукт",
                            command=lambda: AddToDatabase(name_entry, category_entry, protein_entry, fat_entry, carbohydrates_entry, kcal_entry, products, combobox_diary))
    add_button.pack(anchor=CENTER, pady=10)

    # Кнопка очистки базы продуктов
    clear_button = ttk.Button(base_frame, text="Очистить базу",
                               command=lambda: clear_database(products, combobox_diary))
    clear_button.pack(anchor=CENTER, pady=10)

    root.mainloop()  # Запуск основного цикла программы
