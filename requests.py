import psycopg2 as sql
import pandas as pd
#присоединяемся к базе данных
conn = sql.connect(

    host="postgrepro.dc-edu.ru",
    port="5432",
    dbname="dbstud",
    user="bk_467685_2025",
    password="bk_467685",
    client_encoding="UTF8"
)
cursor = conn.cursor()

def requests_print():
    print("""Выберите запрос(введите соответствующую цифру):
    1. Получить все товары определённой категории.
    2. Получить все заказы за определённый день.
    3. Показать содержимое конкретного заказа.
    4. Получить заказы, принадлежащие определённому заказчику.
    5. Получить список всех комбо, с количеством пирожных и их названием.
    6. Получить сумму заказов определённого торта/пирожного/комбо
    7. Получить список всех заказчиков
    Ctrl+C, чтобы завершить программу
    """)

def table_print(curs, res):
    columns = [x[0] for x in cursor.description]
    db = pd.DataFrame(result, columns=columns)
    print()
    print('Ваш запрос:')
    print()
    print(db.to_string(index=False))
    print()

while True:
    requests_print()
    try:
        user_input = int(input())
        if not (1 <= user_input <= 7):
            raise ValueError("Значение должно быть в пределах от 1 до 7 (включительно)")

        match user_input:
            case 1:
                print("""Введите категорию (цифру):
                1. Торты
                2. Пирожные
                3. Комбо (Мини пирожные)
                """)
                user1_input = int(input())
                match user1_input:
                    case 1:
                        cursor.execute("SELECT id,name,category FROM menu WHERE category ILIKE 'Торты'")
                        result = cursor.fetchall()

                        table_print(cursor, result)
                    case 2:
                        cursor.execute("SELECT id,name,category FROM menu WHERE category ILIKE "
                                       "'Пирожное'")
                        result = cursor.fetchall()
                        table_print(cursor, result)
                    case 3:
                        cursor.execute("SELECT id,name,count FROM combo")
                        result = cursor.fetchall()
                        table_print(cursor, result)
            case 2:
                print("""Введите год-месяц-день в формате (2025-05-05""")
                user1_input = input()
                cursor.execute(f"SELECT * FROM orders WHERE time_order ILIKE {user1_input}")
                result = cursor.fetchall()
                table_print(cursor, result)
            case 3:
                print("""Введите номер заказа: (от 1 до 555)""")
                user1_input = int(input())
                cursor.execute(""""""

                result = cursor.fetchall()
                table_print(cursor, result)



    except Exception as e:
        print(f"Ошибка: {e}")

