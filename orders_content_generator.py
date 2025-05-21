import csv
import random

def generate_orders_content_csv(filename):
    num_orders = 555
    order_ids = list(range(1, num_orders + 1))
    random.shuffle(order_ids)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "orders_id", "id_good", "id_combo", "count_good", "count_combo"])

        for i, order_id in enumerate(order_ids, start=1):
            # Генерация id_good и count_good
            num_goods = random.randint(1, 5)
            id_good = [random.randint(1, 15) for _ in range(num_goods)]
            count_good = [random.randint(1, 10) for _ in range(num_goods)]

            # Генерация id_combo и count_combo
            num_combos = random.randint(0, 3)  # можно 0, чтобы иногда массивы были пустыми
            id_combo = [random.randint(1, 5) for _ in range(num_combos)]
            count_combo = [random.randint(1, 5) for _ in range(num_combos)]

            # Преобразование списков в строку в SQL-совместимом формате
            id_good_str = "{" + ",".join(map(str, id_good)) + "}"
            id_combo_str = "{" + ",".join(map(str, id_combo)) + "}"
            count_good_str = "{" + ",".join(map(str, count_good)) + "}"
            count_combo_str = "{" + ",".join(map(str, count_combo)) + "}"

            writer.writerow([i, order_id, id_good_str, id_combo_str, count_good_str, count_combo_str])

# Вызов генерации
generate_orders_content_csv("orders_content.csv")
