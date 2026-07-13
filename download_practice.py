import pandas as pd
import sqlite3
import random

orders = [
    (1, 3),  #商品ID=1を3個
    (2, 5),  #商品ID=2を5個
    (3, 1),  #商品ID=3を1個
    (4, 3),  #商品ID=4を3個
    (5, 5),  #商品ID=5を5個
    (6, 1)  #商品ID=6を1個
]

randam = ["レタス","トマト","なすび","ピーマン"]
randim = ["ハンバーグ","八宝菜","麻婆豆腐"]
randum = ["コーラ","サイダー","お茶"]

products2 = [
    (random.choice(randam),"野菜",500),
    (random.choice(randim),"惣菜",300),
    (random.choice(randum),"飲料",400),
    ("チョコ","お菓子",180)
]

id = int(input("削除するID:"))

conn = sqlite3.connect("shop.db")

cur = conn.cursor()

cur.executemany("""INSERT INTO orders (商品ID, 数量) VALUES (?,?)""", orders)

cur.executemany("""INSERT INTO products2 (品物, 種類, 金額) VALUES (?,?,?) """, products2)

cur.execute("""UPDATE products2 SET 金額 = ? WHERE id = ?""", (400, 3))

cur.execute("""DELETE FROM products2 WHERE id = ?""",(id,))

conn.commit()

df = pd.read_sql("SELECT * FROM products2 WHERE 金額 >= 400 ORDER BY 金額 ASC;", conn)

df2 = pd.read_sql("SELECT 品物, 数量 FROM products2 LEFT JOIN orders ON products2.id = orders.商品ID", conn)

print(df)

print(df2)

conn.close()

