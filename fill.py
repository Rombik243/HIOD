import psycopg2 as sql
def drop():
    cursor.execute("DROP TABLE IF EXISTS menu CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS combo CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS orders CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS goods_link CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS combos_link CASCADE;")

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
                        CREATE TABLE combo(id SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL REFERENCES menu(name), cake_id INT REFERENCES menu(id), count INT);
                        CREATE TABLE orders(id SERIAL PRIMARY KEY, time_order TIMESTAMP, time_deliv TIMESTAMP, address VARCHAR(80), seller VARCHAR(80));
                        CREATE TABLE goods_link(order_id INT NOT NULL REFERENCES orders(id), id_good INT REFERENCES menu(id) NOT NULL, count_good INT NOT NULL, PRIMARY KEY(order_id, id_good));
                        CREATE TABLE combos_link(order_id INT NOT NULL REFERENCES orders(id), id_combo INT NOT NULL REFERENCES combo(id), count_combo INT NOT NULL, PRIMARY KEY(order_id, id_combo));"""

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

with open("goods_link.csv", "r", encoding = 'utf-8') as f:
    cursor.copy_expert("""
        COPY goods_link (order_id, id_good, count_good)
        FROM STDIN
        DELIMITER ','
        CSV HEADER;
    """, f)

with open("combos_link.csv", "r", encoding = 'utf-8') as f:
    cursor.copy_expert("""
        COPY combos_link (order_id, id_combo, count_combo)
        FROM STDIN
        DELIMITER ','
        CSV HEADER;
    """, f)
# Фиксируем изменения в БД
#1
#conn.commit()

print("Таблицы успешно создана!")
