import sqlite3

def initiate_db():
    connection = sqlite3.connect("Products_base.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        """)

    products = cursor.execute("SELECT id FROM Products")
    if products.fetchone() is None:
        for i in range(1, 5):
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                           (f"Product{i}", f"Description{i}", f"{i * 10}"))

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect("Products_base.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    connection.close()

    return products

def add_user(username, email, age):
    connection = sqlite3.connect("Products_base.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"{username}", f"{email}", f"{age}", "1000"))

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect("Products_base.db")
    cursor = connection.cursor()
    result = True
    products = cursor.execute("SELECT id FROM Users WHERE username = ?", (f"{username}",))
    if products.fetchone() is None:
        result = False
    return result