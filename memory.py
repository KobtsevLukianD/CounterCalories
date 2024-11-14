import pickle
import os

# Функция для сохранения полей products и names
def file_save(base, filename):
    # Сохраняем только два поля объекта: products и names
    data = {"products": base.products, "names": base.names}
    with open(filename, "wb") as file:
        pickle.dump(data, file)

# Функция для загрузки полей products и names из файла
def file_load(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data  # Возвращаем словарь с полями products и names
    return None

# Функция для очистки файла
def file_clear(filename):
    if os.path.exists(filename):
        os.remove(filename)
