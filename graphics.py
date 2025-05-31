

import psycopg2 as sql
import pandas as pd
import matplotlib.pyplot as plt

from requests import user1_input


def graf():
    print('Введите номер запроса:')
    print('''
    1. Соотношение тортов, пирожных и мини пирожных
    2. Соотношение сумм заказов конкретных изделий
    
    0. Завершить программу''')

conn = sql.connect(

    host="postgrepro.dc-edu.ru",
    port="5432",
    dbname="dbstud",
    user="bk_467685_2025",
    password="bk_467685",
    client_encoding="UTF8"
)
cursor = conn.cursor()

while True:
    try:
        graf()
        user_input = int(input())
        match user_input:
            case 1:
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM menu
                               WHERE category = 'Торты'
                               """)
                cakes_count = cursor.fetchone()[0]

                # SQL-запрос для подсчета обычных пирожных (category='Пирожное' AND subcategory=0)
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM menu
                               WHERE category = 'Пирожное'
                                 AND subcategory = FALSE
                               """)
                pastries_count = cursor.fetchone()[0]

                # SQL-запрос для подсчета мини пирожных (category='Пирожное' AND subcategory=1)
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM menu
                               WHERE category = 'Пирожное'
                                 AND subcategory = TRUE
                               """)
                mini_pastries_count = cursor.fetchone()[0]

                # Формируем данные для диаграммы
                data = {
                    'Торты': cakes_count,
                    'Пирожные': pastries_count,
                    'Мини пирожные': mini_pastries_count
                }

                # Создаем круговую диаграмму
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%',
                       startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99'],
                       explode=(0.05, 0, 0))
                ax.set_title('Соотношение тортов, пирожных и мини пирожных', pad=20)
                ax.axis('equal')
                plt.show()
            case 2:
                cursor.execute("SELECT COUNT(*) FROM menu")
                all_count = cursor.fetchone()[0]
                a = [0] * all_count
                for i in range(len(a)):
                    user1_input = i + 1 # id товара из меню
                    cursor.execute(f"""SELECT name FROM menu WHERE id = {user1_input}""")
                    cake_name = cursor.fetchall()[0][0]

                    cursor.execute(f"""
                                        SELECT SUM(count_good[array_position(id_good, {user1_input})])
                                        FROM orders_content
                                        WHERE {user1_input} = ANY(id_good); """)

                    result = cursor.fetchall()[0][0] or 0

                    cursor.execute("SELECT COUNT(*) FROM menu")
                    count_menu = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM combo")
                    count_combo = cursor.fetchone()[0]
                    user1_input -= (count_menu - count_combo)
                    cursor.execute(f"""
                                        SELECT SUM(count_combo[array_position(id_combo, {user1_input})])
                                        FROM orders_content
                                        WHERE {user1_input} = ANY(id_combo); """)
                    result2 = cursor.fetchall()[0][0] or 0
                    a[i] = result+result2

            case 0:
                exit(0)

    except Exception as e:
        print(f"Ошибка: {e}")


