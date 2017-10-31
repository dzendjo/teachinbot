import socket
from threading import Thread
from config import token
from db_mapping_classes import Category, Lecturer, Lecture, DBInit
from sqlalchemy import inspect
import json
import sys


class Teachinbot:

    def __init__(self):
        self.token = token
        self.session = DBInit().get_session()
        self.class_lookup = {
            'Lecturer': Lecturer,
            'Lecture': Lecture,
            'Category': Category
        }

    def get_all_lecturies(self):
        return self.session.query(Lecture).all()

    def get_all_categories(self):
        return self.session.query(Category).all()

    def get_all_lecturers(self):
        return self.session.query(Lecturer).all()

    def add_lecture(self, lecture):
        self.session.add(lecture)
        self.session.commit()

    def add_category(self, category):
        self.session.add(category)
        self.session.commit()

    def add_lecturer(self, lecturer):
        if isinstance(lecturer, Lecturer):
            self.session.add(lecturer)
            self.session.commit()
        elif isinstance(lecturer, str):
            self.session.add(Lecturer(lecturer))
            self.session.commit()
        else:
            raise Exception('Непонятный формат добавления лектора')


    def del_lecture(self, lecture):
        self.session.delete(lecture)
        self.session.commit()

    def del_category(self, category):
        self.session.delete(category)
        self.session.commit()

    def del_lecturer(self, lecturer_name):
        for lecturer in self.session.query(Lecturer).all():
            if lecturer.name == lecturer_name:
                self.session.delete(lecturer)
                self.session.commit()
                return True
        print("Удаление не удалось")
        return False

    def print_all_db(self):
        print(self.get_all_lecturies())
        print(self.get_all_lecturers())
        print(self.get_all_categories())

    def find_lecturer(self, lecturer_name):
        lecturers = self.session.query(Lecturer).all()
        if isinstance(lecturer_name, str):
            for lecturer in lecturers:
                if str(lecturer_name).lower == str(lecturer.name).lower():
                    return self.session.query(Lecturer).filter(Lecturer.name == lecturer_name).first()
        return None

    def find_category(self, category_name):
        categories = self.session.query(Category).all()
        if isinstance(category_name, str):
            for category in categories:
                if str(category_name).lower() == str(category.name).lower():
                    return self.session.query(Category).filter(Category.name == category_name).first()
        return None

    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    def dump(self, filename, data):
        with open(filename, 'w') as f:
            result_json = []
            for item in data:
                item_class_name = item.__class__.__name__
                item_as_dict = self.object_as_dict(item)
                del item_as_dict['id']
                item_json = {item_class_name : item_as_dict}
                result_json.append(item_json)
            json.dump(result_json, f)


    def load(self, filename):
        with open(filename, 'r') as f:
            res = json.loads(f.read())
            for item in res:
                item_class_name = list(item.keys())[0]
                item_params = item[item_class_name]
                new_obj = self.class_lookup[item_class_name](**item_params)
                print(new_obj)
                self.session.add(new_obj)
            self.session.commit()
        return True

    def save_lecturers(self):
        data = self.get_all_lecturers()
        t = Thread(target=self.dump, args=('all_lecturers.json', data))
        t.run()

    def load_lecturers(self):
        t = Thread(target=self.load, args=('all_lecturers.json',))
        res = t.run()
        return res

    def save_lecturies(self):
        data = self.get_all_lecturies()
        t = Thread(target=self.dump, args=('all_lecturies.json', data))
        t.run()

    def load_lecturies(self):
        t = Thread(target=self.load, args=('all_lecturies.json',))
        res = t.run()
        return res

    def save_categories(self):
        data = self.get_all_categories()
        t = Thread(target=self.dump, args=('all_categories.json', data))
        t.run()

    def load_categories(self):
        t = Thread(target=self.load, args=('all_categories.json',))
        res = t.run()
        return res

    def save_all(self):
        data = []
        for item in self.get_all_categories():
            data.append(item)
        for item in self.get_all_lecturers():
            data.append(item)
        for item in self.get_all_lecturies():
            data.append(item)
        t = Thread(target=self.dump, args=('all_data.json', data))
        t.run()

    def load_all(self):
        t = Thread(target=self.load, args=('all_data.json',))
        res = t.run()
        return res




bot = Teachinbot()

def simple_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 9999))
    print('Cервер запущен...')
    sock.listen()
    conn, addr = sock.accept()
    print('К нам попался клиент', addr)

    print('Отправляем ему "троянца"...')
    # Отсылаем опасный объект "доверчивому" клиенту
    conn.send(pickle.dumps(EvilPayload()))

print(sys.argv)
if '-sm' in sys.argv:
    #Run script with a server mode
    pass

# #Печатаем старую базу:
# bot.print_all_db()

# #Скидываем все таблицы в файл
# bot.save_lecturers()
# bot.save_categories()
# bot.save_lecturies()
# bot.save_all()

# #Загружаем все таблицы из файлов в БД
# dict = bot.load_lecturers()
# bot.load_lecturies()
# bot.load_categories()
# bot.load_all()

# bot.print_all_db()




