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
    3. Получить детализацию конкретного заказа
    4. Получить заказы, принадлежащие определённому заказчику.
    5. Получить список топ 5 популярных товаров
    6. Получить отчёт по заказам за месяц с группировкой по магазинам
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
                print("""Введите идентификационный номер заказа: """)
                user1_input = int(input())
                cursor.execute(f"""
                SELECT 'Товар' AS type, m.name, gl.count_good AS count
                FROM goods_link gl
                JOIN menu m ON gl.id_good = m.id
                WHERE gl.order_id = {user1_input}
                
                UNION ALL
                
                SELECT 'Комбо' AS type, c.name, cl.count_combo AS count
                FROM combos_link cl
                JOIN combo c ON cl.id_combo = c.id
                WHERE cl.order_id ={user1_input};""")

                result = cursor.fetchall()
                table_print(cursor, result)

            case 4:
                print('Введите фамилию заказчика:')
                user1_input = input()
                cursor.execute(f"""SELECT * FROM orders WHERE seller LIKE '{user1_input + " %"}'""")
                result = cursor.fetchall()
                table_print(cursor, result)

            case 5:
                cursor.execute("""
                SELECT m.name, SUM(goods_link.count_good) AS total_count
                FROM goods_link
                JOIN menu m ON goods_link.id_good = m.id
                GROUP BY m.name
                ORDER BY total_count DESC
                LIMIT 5;""")
                result = cursor.fetchall()
                table_print(cursor, result)

            case 6:
                print("""Введите год-месяц в формате (2025-05)""")
                user1_input = input()
                user1_input += '-01'
                query = """
                        SELECT seller, 
                               COUNT(*) AS orders_count, 
                               SUM( 
                                       (SELECT COALESCE(SUM(gl.count_good), 0) 
                                        FROM goods_link gl 
                                        WHERE gl.order_id = o.id) + 
                                       (SELECT COALESCE(SUM(cl.count_combo), 0) 
                                        FROM combos_link cl 
                                        WHERE cl.order_id = o.id) 
                               )        AS items_count
                        FROM orders o
                        WHERE time_order BETWEEN
                                  TO_TIMESTAMP(%s, 'YYYY-MM-DD')
                                  AND
                                  (TO_TIMESTAMP(%s, 'YYYY-MM-DD') + INTERVAL '1 month - 1 day')
                        GROUP BY seller
                        ORDER BY orders_count DESC; 
                        """

                # Выполняем запрос с параметрами
                cursor.execute(query, (user1_input, user1_input))
                result = cursor.fetchall()
                table_print(cursor, result)

            case 7:
                cursor.execute("""SELECT DISTINCT seller FROM orders""")

                result = cursor.fetchall()
                table_print(cursor, result)

    except Exception as e:
        print(f"Ошибка: {e}")


conn.close()
cursor.close()