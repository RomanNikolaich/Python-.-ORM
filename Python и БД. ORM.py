import psycopg2
import configparser
import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import datetime


'''Помимо классической кодовой конструкции из модуля 'models' сделаны цикличные функции
   для заполнения таблиц. Также при заполнении факта продажи (заполнение таблицы sale)
   устанавливается автоматически дата продажи'''

Base = declarative_base()

config = configparser.ConfigParser()
config.read('config.ini')
postgres_pass = config['DataBase']['postgres_pass']
type_db = config['DataBase']['type_db']
login = config['DataBase']['login']
data_base = config['DataBase']['data_base']


DSN = f'{type_db}://{login}:{postgres_pass}@localhost:5432/{data_base}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)

session = Session()

# Функция для добавления издательства (заполнения таблицы publisher)
def publisher():
    p = 'д'
    while p == 'д':
        name1 = input('Введите название издательства: ')
        pub1 = Publisher(name=name1)
        session.add(pub1)
        p = input("Введите 'д', если хотите добавить еще издательство: ")
    return session.commit()
#pub1 = publisher()

# Функция для добавления книг (заполнения таблицы book)
def book():
    b = 'д'
    while b == 'д':
        book = input('Введите название книги: ')
        autor = input('Введите имя автора: ')
        q = input('Введите номер издания: ')
        book1 = Book(title=book, autor_name=autor, id_publisher=q)
        session.add(book1)
        b = input("Введите 'д', если хотите добавить еще книгу: ")
    return session.commit()
#book1 = book()

# Функция для добавления магазинов (заполнения таблицы shop)
def shop():
    s = 'д'
    while s == 'д':
        name1 = input('Введите название магазина: ')
        shop1 = Shop(name=name1)
        session.add(shop1)
        s = input("Введите 'д', если хотите добавить еще магазин: ")
    return session.commit()
#shop1 = shop()

# Функция для добавления экземпляров (заполнения таблицы stock)
def stock():
    s = 'д'
    while s == 'д':
        id_book1 = input('Введите номер книги: ')
        id_shop1 = input('Введите номер магазина: ')
        count1 = input('Введите количество экзепляра: ')
        stock1 = Stock(id_book=id_book1, id_shop=id_shop1, count=count1)
        session.add(stock1)
        s = input("Введите 'д', если хотите добавить еще: ")
    return session.commit()
#stock1 = stock()


# Функция для создания продажи c автоматической отметкой даты продажи (заполнения таблицы sale)
# и с автоматическим уменьшением
# количества экземпляра книги в таблице stock

def sale():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    s = 'д'
    while s == 'д':
        price1 = input('Введите цену книги в формате 00.00: ')
        id_stock1 = input('Введите номер экземпляра: ')
        count1 = int(input('Введите количество проданных копий: '))
        sale1 = Sale(price=price1, date_sale=current_date, id_stock=id_stock1, count=count1)
        session.add(sale1)
        session.query(Stock).filter(Stock.id == id_stock1).update({'count': Stock.count - count1})                  
        s = input("Введите 'д', если хотите добавить еще продажу: ")
        return session.commit()
sale()

# Функция для вывода фактов покупки по названию издательсва
def sale_facts():
    name = input('Введите название издательства: ')
    subq = session.query(Publisher).filter(Publisher.name == name).subquery()
    subq2 = session.query(Book).join(subq, Book.id_publisher==subq.c.id).subquery()
    subq3 = session.query(Stock).join(subq2, Stock.id_book==subq2.c.id).subquery()
    for g in session.query(Sale).join(subq3, Sale.id_stock==subq3.c.id).all():
        print(g)
#sale_facts()

# Функция для вывода фактов покупки по названию книги
def sale_facts_2():
    book_title = input('Введите название издательства: ')
    subq2 = session.query(Book).filter(Book.title==book_title).subquery()
    subq3 = session.query(Stock).join(subq2, Stock.id_book==subq2.c.id).subquery()
    for g in session.query(Sale).join(subq3, Sale.id_stock==subq3.c.id).all():
        print(g)
#sale_facts_2()


session.close()




