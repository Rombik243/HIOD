import psycopg2 as sql
def drop():
    cursor.execute("DROP TABLE IF EXISTS menu")
    cursor.execute("DROP TABLE IF EXISTS combo")
    cursor.execute("DROP TABLE IF EXISTS orders_content")
    cursor.execute("DROP TABLE IF EXISTS orders")

# Подключаемся к серверу PostgreSQL (без указания dbname!)

conn = sql.connect(

    host="postgrepro.dc-edu.ru",
    port="5432",
    dbname="dbstud",
    user="bk_467685_2025",
    password="bk_467685",

)
conn.autocommit = True  # Для создания БД нужен autocommit

# Создаём курсор для выполнения SQL-запросов
cursor = conn.cursor()
drop()
# SQL-запрос для создания таблицы
create_table_query = """CREATE TABLE menu (id SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL, category VARCHAR(20) NOT NULL, subcategory BOOL);
                        CREATE TABLE combo(id SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL, cake_id SMALLINT, count SMALLINT);
                        CREATE TABLE orders_content(id SERIAL PRIMARY KEY, orders_id INTEGER, id_good SMALLINT[], id_combo SMALLINT[], count_good SMALLINT[], count_combo SMALLINT[]);
                        CREATE TABLE orders(id SERIAL PRIMARY KEY, time_order TIMESTAMP, time_deliv TIMESTAMP, address VARCHAR(80), seller VARCHAR(80));"""

# Выполняем запрос
cursor.execute(create_table_query)

with open("menu.csv", "r", encoding = 'utf-8') as f:
    cursor.copy_expert("""
        COPY menu (id, name, category, subcategory)
        FROM STDIN
        DELIMITER ','
        CSV HEADER;
    """, f)

with open("combo.csv", "r", encoding = 'utf-8') as f:
    cursor.copy_expert("""
        COPY combo (id, name, cake_id, count)
        FROM STDIN
        DELIMITER ','
        CSV HEADER;
    """, f)

with open("orders.csv", "r", encoding = 'utf-8') as f:
    cursor.copy_expert("""
        COPY orders (id, time_order, time_deliv, address, seller)
        FROM STDIN
        DELIMITER ','
        CSV HEADER;
    """, f)

with open("orders_content.csv", "r", encoding = 'utf-8') as f:
    cursor.copy_expert("""
        COPY orders_content (id, orders_id, id_good, id_combo, count_good, count_combo)
        FROM STDIN
        DELIMITER ','
        CSV HEADER;
    """, f)
# Фиксируем изменения в БД
#1
#conn.commit()

print("Таблицы успешно создана!")
