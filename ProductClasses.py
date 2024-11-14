# Классы продуктов, использующиеся в базе данных и в холодильнике пользователя.
# Класс Database - база со всеми продуктами в приложении. В нем хранится информация о категории, наименовании и КБЖУ
  # Методы для добавления, удаления и редактирования базы
# У классов для холодильника определены методы, позволяющие узнать, просрочен ли продукт и много ли ему осталось до истечения срока годности

from datetime import datetime, date

class BaseProduct():
    "Экземпляры этих классов будут храниться в Database"
    def __init__(self, name, category, kcal, protein, fat, carbohydrates):
        self.category = category # Категория товара
        self.name = name # Наименование
        self.kcal = kcal # Килокалории данного продукта на штуку / на 100г 
        self.protein = protein # белков
        self.fat = fat # жиров
        self.carbohydrates = carbohydrates # углеводов
    # TODO: выделить отдельно функционал для продуктов - жидкостей в этом классе и наследниках
    # TODO: написать отдельный класс quantity для более понятного описания количества продукта(штуки, граммы, миллилитры)
    
class Product(BaseProduct):
    "Экземпляры этого класса будут использоваться для составления дневного рациона"
    def __init__(self, mass, quantity, name, category, kcal, protein, fat, carbohydrates):
        self.category = category # Категория товара
        self.name = name # Наименование
        self.mass = mass # Если по массе
        self.quantity = quantity # Если штуками(например, яйца)
        self.kcal = kcal # Килокалории данного продукта на штуку / на 100г 
        self.protein = protein # белков
        self.fat = fat # жиров
        self.carbohydrates = carbohydrates # углеводов
    
class FridgeProduct(Product):
    "Класс-наследник, экземпляры которого будут храниться в нашем холодильнике"
    def __init__(self, mass, quantity, name, purchase_date, expiration_date, category, kcal, protein, fat, carbohydrates):
        self.category = category # Категория товара
        self.name = name # Наименование
        self.purchase_date = purchase_date # Дата приобретения
        self.expiration_date = expiration_date # Дата истечения срока годности
        self.mass = mass # Если по массе
        self.quantity = quantity # Если штуками(например, яйца)
        self.kcal = kcal # Килокалории данного продукта на штуку / на 100г 
        self.protein = protein # белков
        self.fat = fat # жиров
        self.carbohydrates = carbohydrates # углеводов
    
    def is_expired(self):
        "Возвращает True, если продукт просрочен"
        if date.today > self.expiration_date:
            return True
        return False
    
    def get_remaining_days(self):
        "Возвращает разницу между датой истечения срока годности и сегодняшней датой"
        return self.expiration_date - date.today
    
class ProductDatabase():
    "Список всех существующих в приложении продуктов"
    
    products = {} # Словарь словарей
    
    names = [] # Список со всеми названиями продуктов
    
    def add_product(self, product):
        "Вносим новый продукт класса BaseProduct в базу данных"
        if not (product.category in self.products):  # Создаем новую категорию
            self.products[product.category] = {}
        elif product.name in self.products[product.category]: # Проверка на попытку повторно внести уже существующий продукт
            return
        self.products[product.category][product.name] = product
        
        self.names.append(product.name)
        
    def remove_product(self, product):
        "Удаляем продукт из базы данных"
        if not (product.category in self.products) and not (product.name in self.products[product.category]): # Такого продукта нет
            return
        del self.products[product.category][product.name] # Удаляем продукт
        self.names.remove(product.name)
        if self.products[product.category] == {}: # Если категория пустая, удаляем и категорию
            del self.products[product.category]
        
    def clear(self):
        self.products = {}
        self.names = []        
    
    def change_parameters(self, old_product, new_product):
        return
        # TODO: если в базе необходимо редактировать какой-либо продукт(вплоть до изменеия названия или категории)