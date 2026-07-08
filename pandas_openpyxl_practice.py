import pandas as pd

sum = 0

df = pd.read_csv("apple.csv")

print(df["価格"].sum())
print(df.groupby("種類")["価格"].sum())
print(df[df["価格"] >= 150])
print(df.sort_values("価格", ascending=False))




"""
df = pd.read_csv("apple.csv" )

print(df["売上"].sum())
print(df["売上"].mean())
print(df["売上"].min())
print(df[df["部署"] == "営業"])
print(df[df["売上"] >= 100000])
print(df.groupby("部署")["売上"].sum())
print(df.sort_values("売上", ascending=False))
df.to_excel("結果.xlsx", index=False)
"""
