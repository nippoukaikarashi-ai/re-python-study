import sqlite3
import pandas as pd

conn = sqlite3.connect("shop.db")

df = pd.read_csv("apple.csv")

df.to_sql("products", conn, if_exists="replace", index=False)

cur = conn.cursor()

cur.execute("""CREATE TABLE orders(注文ID INTEGER PRIMARY KEY AUTOINCREMENT, 商品ID INTEGER NOT NULL, 数量 INTEGER NOT NULL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS products2(id INTEGER PRIMARY KEY AUTOINCREMENT, 品物 TEXT NOT NULL, 種類 TEXT NOT NULL, 金額 INTEGER NOT NULL)""")

conn.commit()

conn.close()

print("保存完了!")
