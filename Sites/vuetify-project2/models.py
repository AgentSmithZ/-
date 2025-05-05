import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(role_id) REFERENCES roles(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    price REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_order TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    table_number INTEGER NOT NULL,
    guest_count INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    amount INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(dish_id) REFERENCES menu(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cooking_process (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_item_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'waiting',
    FOREIGN KEY(order_item_id) REFERENCES order_items(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

cursor.execute("INSERT OR IGNORE INTO roles (role) VALUES ('Admin')")
cursor.execute("INSERT OR IGNORE INTO roles (role) VALUES ('Waiter')")
cursor.execute("INSERT OR IGNORE INTO roles (role) VALUES ('Cook')")

cursor.execute("INSERT OR IGNORE INTO users (nickname, password, role_id) VALUES ('admin', '123456', 1)")
cursor.execute("INSERT OR IGNORE INTO users (nickname, password, role_id) VALUES ('waiter', '654321', 2)")
cursor.execute("INSERT OR IGNORE INTO users (nickname, password, role_id) VALUES ('cook', '321456', 3)")

cursor.execute("INSERT OR IGNORE INTO menu (title, type, price) VALUES ('Борщ', 'Еда', '200')")
cursor.execute("INSERT OR IGNORE INTO menu (title, type, price) VALUES ('Стейк', 'Еда', '1700')")
cursor.execute("INSERT OR IGNORE INTO menu (title, type, price) VALUES ('Кофе', 'Напитки', '100')")
cursor.execute("INSERT OR IGNORE INTO menu (title, type, price) VALUES ('Пирожок', 'Еда', '50')")

# Вставляем новые корректные заказы
cursor.execute("INSERT OR IGNORE INTO orders (date_order) VALUES ('2025-04-29')")
cursor.execute("INSERT OR IGNORE INTO orders (date_order) VALUES ('2025-04-30')")
cursor.execute("INSERT OR IGNORE INTO orders (date_order) VALUES ('2025-05-01')")

# Получим последний созданный id заказа
last_order_id = cursor.lastrowid

# Теперь заполним table order_items для первого заказа
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (last_order_id, 1))
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (last_order_id, 3))

# Аналогично поступим с остальными заказами
# Предположим, второй заказ сделан позже
second_last_order_id = last_order_id - 1
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (second_last_order_id, 2))
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (second_last_order_id, 5))

# Третий заказ
third_last_order_id = second_last_order_id - 1
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (third_last_order_id, 2))
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (third_last_order_id, 3))
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (third_last_order_id, 4))

# Первый заказ (предполагаем, что первый сделан ранее остальных)
first_order_id = third_last_order_id - 1
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (first_order_id, 1))
cursor.execute("INSERT INTO order_items (order_id, dish_id) VALUES (?, ?)", (first_order_id, 2))

# Фиксация изменений и закрытие соединения
db.commit()
db.close()