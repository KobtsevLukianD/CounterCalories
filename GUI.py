# Графический интерфейс
# В этом файле программируется десктопное приложение с использованием библиотеки tkinter 

import tkinter as tk # Библиотека для создания интерфейса
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import ProductClasses # Файл с классами продуктов
from ProductClasses import Product, ProductDatabase, BaseProduct

import memory # Сохранение базы

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
    "На вход поступает строка - название продукта. Функция возвращает объект класса Product, взаимодействуя с Database"
    for outer_key, inner_dict in base.products.items(): # Пробегаем по всем категориям
        # TODO: В программе пока никак не используются категории товаров
        for inner_key, obj in inner_dict.items(): # Пробегаем по всем продуктам данной категории
            if obj.name == name:
                return Product(mass, quantity, name, category = obj.category, kcal = obj.kcal, protein = obj.protein, fat = obj.fat, carbohydrates = obj.carbohydrates)

def centering_in_window(window, width, height):
    "Задаем размер окна и размещаем его по центру экрана"
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")            

def run_program():
    "Отсюда начинает работать графическая часть приложения"
    root = Tk() # Создаем корневой объект
    root.title("Счетчик калорий") # Заголовок
    root_width, root_height = 400, 500 # Ширина и высота окна
    centering_in_window(root, root_width, root_height)
    
    # root.resizable(False, False) # Фиксируем размер окна
    
    # TODO: Убрать иконку в левом верхнем углу
    # TODO: Подумать над тем чтобы убрать title
    
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
    diary_label1 = ttk.Label(diary_frame, text="Дневник питания")
    diary_label1.pack(anchor=CENTER)

    # Набор продуктов (один за одним - выпадающие списки)

    # Список наименований продуктов
    products = [" "] + base.names
    
    # Вспомогательная функция для обновления всех выпадающих списков на diary_frame
    def update_combobox_values(combobox_diary, products):
        for row in combobox_diary:
            for combobox in row:
                # Обновляем только те combobox, где список значений не ограничен (" " не является единственным значением)
                if (combobox["values"] != (" ",) or len(row) < 2):
                    combobox["values"] = products




    selections = [[] for i in range(5)]  # Список списков. Во внутреннем списке лежат классы Product
    # Наименование приемов пищи
    diary_labels = [ttk.Label(diary_frame, text="Завтрак"),
                    ttk.Label(diary_frame, text="Обед"),
                    ttk.Label(diary_frame, text="Полдник"),
                    ttk.Label(diary_frame, text="Ужин"),
                    ttk.Label(diary_frame, text="Перекус")]

    # Список списков выпадающих меню для разных приемов пищи
    combobox_diary = [[ttk.Combobox(diary_frame, values=products, state="readonly")] for i in range(5)]

    # Функция для вычисления сумм калорий, белков, жиров и углеводов
    def calculate_totals():
        total_kcal = 0
        total_protein = 0
        total_fat = 0
        total_carbohydrates = 0

        for n in range(len(selections)):
            for i in range(len(selections[n])):
                product = selections[n][i]
                # Умножаем на количество
                total_kcal += product.kcal
                total_protein += product.protein
                total_fat += product.fat
                total_carbohydrates += product.carbohydrates

        # Обновляем значения в полях
        kcal_label_value.config(text=f"{total_kcal:.2f} ккал")
        protein_label_value.config(text=f"{total_protein:.2f} г")
        fat_label_value.config(text=f"{total_fat:.2f} г")
        carbohydrates_label_value.config(text=f"{total_carbohydrates:.2f} г")

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
    calculate_totals()

    # Функция для обновления значений после выбора продуктов
    def diary_selection(event, combobox_diary, selections, frame, products, labels, n, m):
        "Появляется меню для выбора количества выбранного продукта, а затем полученные данные заносятся в словарь"
        choice = combobox_diary[n][m].get()
        
        # Если выбран пустой вариант, удаляем комбо-бокс
        if str(choice) == " ":
            if len(combobox_diary[n]) > 1 and m != len(combobox_diary[n]) - 1:
                combobox_diary[n][m].pack_forget()
                combobox_diary[n].pop(m)
                selections[n].pop(m)
        else:
            # Сохраняем выбранный продукт и добавляем его в selections
            selections[n].append(product_by_name(choice, 100, 1))
            # Оставляем только пустой вариант в текущем комбо-боксе, чтобы нельзя было выбрать снова
            combobox_diary[n][m]["values"] = [" "]
            
            # Добавляем новый комбо-бокс в текущем приеме пищи
            new_combobox = ttk.Combobox(frame, values=products, state="readonly")
            combobox_diary[n].insert(m + 1, new_combobox)  # Вставляем новый комбо-бокс сразу после текущего
            new_combobox.pack(anchor=CENTER)
            
            # Устанавливаем событие для нового комбо-бокса
            new_combobox.bind("<<ComboboxSelected>>",
                            lambda event, idx1=n, idx2=m + 1: 
                            diary_selection(event, combobox_diary, selections, frame, products, labels, idx1, idx2))
            
        for i in range(len(combobox_diary)):
            labels[i].pack_forget()
            for j in range(len(combobox_diary[i])):
                combobox_diary[i][j].pack_forget()

        # Обновляем отображение списка приемов пищи
        for i in range(len(combobox_diary)):
            labels[i].pack(anchor=CENTER)
            for j in range(len(combobox_diary[i])):
                combobox_diary[i][j].pack(anchor=CENTER)
                combobox_diary[i][j].bind("<<ComboboxSelected>>", 
                                    lambda event, idx1=i, idx2=j: diary_selection(event, combobox_diary, selections, diary_frame, products, diary_labels, idx1, idx2))

        # Пересчитываем итоговые значения
        calculate_totals()
    
    # Внешний цикл проходит по приемам пищи, внутренний - по всем спискам внутри одного приема пищи
    for i in range(len(combobox_diary)):
        diary_labels[i].pack(anchor=CENTER)
        for j in range(len(combobox_diary[i])):
            combobox_diary[i][j].pack(anchor=CENTER)
            combobox_diary[i][j].bind("<<ComboboxSelected>>", 
                                    lambda event, idx1=i, idx2=j: diary_selection(event, combobox_diary, selections, diary_frame, products, diary_labels, idx1, idx2))
    
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

        # Функция для добавления продукта в базу данных
    def AddToDatabase():
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
            
            # Добавляем продукт в базу данных
            base.add_product(BaseProduct(name, category, kcal, protein, fat, carbohydrates))
            
            # Обновляем список продуктов
            products.clear()
            products.extend([" "] + base.names)  # обновленный список
            
            # Обновляем только пустые выпадающие списки на diary_frame
            update_combobox_values(combobox_diary, products)

            # Очистка полей после добавления
            name_entry.delete(0, END)
            category_entry.delete(0, END)
            protein_entry.delete(0, END)
            fat_entry.delete(0, END)
            carbohydrates_entry.delete(0, END)
            kcal_entry.delete(0, END)

            # Сохраняем только поля products и names
            memory.file_save(base, filename)  

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовые значения для белков, жиров, углеводов и калорий.")



    # Кнопка для добавления продукта в базу
    add_button = ttk.Button(base_frame, text="Добавить", command=AddToDatabase)
    add_button.pack(anchor=CENTER, pady=10)
    
    # Функция для очистки базы данных и списка продуктов
    def clear_database():
        memory.file_clear(filename)  # Очистка файла
        base.products.clear()  # Очищаем поле products
        base.names.clear()     # Очищаем поле names
        products.clear()
        products.append(" ")  # Пустое значение для выбора
        
        # Обновляем все выпадающие списки на diary_frame
        update_combobox_values(combobox_diary, products)

    # Кнопка для очистки базы данных
    clear_button = ttk.Button(base_frame, text="Очистить", command=clear_database)
    clear_button.pack(anchor=CENTER, pady=5)
    
    # TODO: Попробовать растащить эту функцию на несколько коротких
    
    root.mainloop()
     