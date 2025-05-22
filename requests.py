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
    
    0. чтобы завершить программу
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
        if not (0 <= user_input <= 7):
            raise ValueError("Значение должно быть в пределах от 0 до 7 (включительно)")

        match user_input:
            case 0:
                exit(0)
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
                print("""Введите год-месяц-день в формате (2025-05-05)""")
                user1_input = input()
                query = f"""
                SELECT * FROM orders 
                WHERE time_order >= '{user1_input}'::timestamp 
                  AND time_order < ('{user1_input}'::date + INTERVAL '1 day')::timestamp
                """
                cursor.execute(query)
                result = cursor.fetchall()
                table_print(cursor, result)
            case 3:
                print("""Введите номер заказа: (от 1 до 555)""")
                user1_input = int(input())
                print()
                cursor.execute(f"SELECT * FROM orders_content WHERE id = {user1_input}")
                result = cursor.fetchall()
                table_print(cursor, result)

                #берём данные из result
                menu1 = result[0][2]
                combo1 = result[0][3]
                menu2 = result[0][4]
                combo2 = result[0][5]
                name_id = result[0][1]
                # получаем имя заказчика
                cursor.execute(f"SELECT seller FROM orders WHERE id = {name_id}")
                result_new = cursor.fetchall()
                name = result_new[0][0]
                df = pd.DataFrame(columns=['id', 'name', 'good', 'count'])

                for i in range(len(menu1)):
                    cursor.execute(f"SELECT name FROM menu WHERE id = {menu1[i]}")
                    good = cursor.fetchall()[0][0]

                    new_row = {'id': user1_input, 'name': name, 'good': good, 'count': menu2[i]}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

                for i in range(len(combo1)):
                    cursor.execute(f"SELECT name FROM combo WHERE id = {combo1[i]}")
                    good = cursor.fetchall()[0][0]

                    new_row = {'id': user1_input, 'name': name, 'good': good, 'count': combo2[i]}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                print(df.to_string(index=False))
                print()
            case 4:
                print('Введите фамилию заказчика:')
                user1_input = input()
                cursor.execute(f"""SELECT * FROM orders WHERE seller LIKE '{user1_input + " %"}'""")
                result = cursor.fetchall()
                table_print(cursor, result)

            case 5:
                cursor.execute(f"""SELECT id,name,count FROM combo """)
                result = cursor.fetchall()
                table_print(cursor, result)

            case 6:
                print('Выберите кондитерское изделие, введите id')
                cursor.execute("SELECT id,name,category FROM menu")
                columns = [x[0] for x in cursor.description]
                result = cursor.fetchall()
                db = pd.DataFrame(result, columns=columns)
                print(db.to_string(index=False))
                user1_input = int(input())
                cursor.execute(f"""SELECT name FROM menu WHERE id = {user1_input}""")
                cake_name = cursor.fetchall()[0][0]

                cursor.execute(f"""
                    SELECT SUM(count_good[array_position(id_good, {user1_input})])
                    FROM orders_content
                    WHERE {user1_input} = ANY(id_good); """)

                result = cursor.fetchall()[0][0] or 0
                user1_input -= 14
                cursor.execute(f"""
                    SELECT SUM(count_combo[array_position(id_combo, {user1_input})])
                    FROM orders_content
                    WHERE {user1_input} = ANY(id_combo); """)
                result2 = cursor.fetchall()[0][0] or 0
                print(f'Заказчики приобрели {cake_name} в количестве {result+result2}')


            case 7:
                cursor.execute("""SELECT DISTINCT seller FROM orders ORDER BY seller""")
                result = cursor.fetchall()
                table_print(cursor, result)

    except Exception as e:
        print(f"Ошибка: {e}")


conn.close()
cursor.close()