import sqlite3
import pandas as pd

conn = sqlite3.connect("shop.db")
df = pd.read_csv("apple.csv")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
    商品 TEXT,
    種類 TEXT,
    価格 INTEGER
)
""")

conn.commit()
conn.close()

print(df)

df.to_sql("prodcts", conn, if_exists="append", index=False)

print("保存完了!")

