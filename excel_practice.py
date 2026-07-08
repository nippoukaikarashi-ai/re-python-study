import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import smtplib
from email.message import EmailMessage
import os


# =========================
# 1. 入出金データ（例）
# =========================
df = pd.read_csv("ren.csv")

# 日付を datetime に変換
df["日付"] = pd.to_datetime(df["日付"])

# 今月のデータだけ抽出（必要なら）
today = datetime.today()
this_month_df = df[
    (df["日付"].dt.year == today.year) &
    (df["日付"].dt.month == today.month)
].copy()

# もしサンプルデータの月と実行月が違う場合、空になるので、
# その場合はサンプルデータ全体を使うようにする^
if this_month_df.empty:
    this_month_df = df.copy()

# 入金/出金集計
income_total = this_month_df.loc[this_month_df["区分"] == "入金", "金額"].sum()
expense_total = this_month_df.loc[this_month_df["区分"] == "出金", "金額"].sum()
balance = income_total + expense_total


# =========================
# 2. Excel(xlsx) 出力
# =========================
xlsx_file = "monthly_cashflow.xlsx"

with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
    # 明細シート
    this_month_df.to_excel(writer, sheet_name="入出金明細", index=False)

    # 集計シート
    summary_df = pd.DataFrame({
        "項目": ["合計入金", "合計出金", "収支"],
        "金額": [income_total, expense_total, balance]
    })
    summary_df.to_excel(writer, sheet_name="月次集計", index=False)

print(f"Excelファイルを作成しました: {xlsx_file}")

# =========================
# 3. PDF 出力
# =========================
pdf_file = "monthly_cashflow.pdf"

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

doc = SimpleDocTemplate(pdf_file, pagesize=A4)
styles = getSampleStyleSheet()
story = []

# タイトル
title_style = styles["Title"]
title_style.fontName = "HeiseiKakuGo-W5"

normal_style = styles["Normal"]
normal_style.fontName = "HeiseiKakuGo-W5"

story.append(Paragraph("今月の入出金管理表", title_style))
story.append(Spacer(1, 12))

# 集計情報
summary_text = (
    f"合計入金: {income_total:,} 円<br/>"
    f"合計出金: {expense_total:,} 円<br/>"
    f"収支: {balance:,} 円"
)
story.append(Paragraph(summary_text, normal_style))
story.append(Spacer(1, 12))

# 明細表用データ
table_data = [["日付", "区分", "金額"]]

for _, row in this_month_df.iterrows():
    table_data.append([
        row["日付"].strftime("%Y-%m-%d"),
        row["区分"],
        f"{row['金額']:,}"
    ])

table = Table(table_data, colWidths=[100, 150, 80, 100])

table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "HeiseiKakuGo-W5"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
]))

story.append(table)
doc.build(story)

print(f"PDFファイルを作成しました: {pdf_file}")


"""
# =========================
# 4. メール送信
# =========================
# 送信元メール情報を設定してください
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "kmhusei55@gmail.com"
SENDER_PASSWORD = "G$jaU89JFJ"   # Gmailならアプリパスワード推奨
RECIPIENT_EMAIL = "destination@example.com"

subject = "今月の入出金管理表"
body = "今月の入出金管理表(Excel / PDF)を送付します。"

msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg.set_content(body)

# 添付ファイル追加
for file_path in [xlsx_file, pdf_file]:
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)

    if file_name.endswith(".xlsx"):
        maintype = "application"
        subtype = "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif file_name.endswith(".pdf"):
        maintype = "application"
        subtype = "pdf"
    else:
        maintype = "application"
        subtype = "octet-stream"

    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

# SMTP送信
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
    smtp.send_message(msg)

print("メール送信が完了しました。")
"""
