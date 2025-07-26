import sqlite3
import pandas as pd


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
''')


df = pd.read_csv('products.csv')


for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO products (name, category, price, stock)
        VALUES (?, ?, ?, ?)
    ''', (row['name'], row['category'], row['price'], row['stock']))

conn.commit()
conn.close()
print("✅ Data loaded into SQLite successfully!")
