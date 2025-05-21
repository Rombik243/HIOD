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

def case3(order_number):


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
                print()
                cursor.execute(f"SELECT * FROM orders_content WHERE id = {user1_input}")
                result = cursor.fetchall()
                table_print(cursor, result)
                print(result)
                menu1 = result[0][2]
                combo1 = result[0][3]
                menu2 = result[0][4]
                combo2 = result[0][5]
                name_id = result[0][1]
                print(menu1,combo1,menu2,combo2,name_id)
                #получаем имя заказчика
                cursor.execute(f"SELECT seller FROM orders WHERE id = {name_id}")
                result_new = cursor.fetchall()
                name = result_new[0][0]
                df = pd.DataFrame(columns=['id', 'name', 'good','count'])

                for i in range(len(menu1)):
                    cursor.execute(f"SELECT name FROM menu WHERE id = {menu1[i]}")
                    good = cursor.fetchall()[0][0]
                    # row = [user1_input, name, good, menu2[i]]
                    # df = pd.concat([df, pd.DataFrame(row)])
                    new_row = {'id': user1_input, 'name': name, 'good': good, 'count': menu2[i]}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

                for i in range(len(combo1)):
                    cursor.execute(f"SELECT name FROM combo WHERE id = {menu1[i]}")
                    good = cursor.fetchall()[0][0]
                    # row = [user1_input, name, good, menu2[i]]
                    # df = pd.concat([df, pd.DataFrame(row)])
                    new_row = {'id': user1_input, 'name': name, 'good': good, 'count': combo2[i]}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                print(df.to_string(index=False))
                print()



    except Exception as e:
        print(f"Ошибка: {e}")

