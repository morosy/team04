import pandas as pd
import mysql.connector

# アクセス情報を access.txt から読み取り
with open('access.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
host, user, password = lines[0], lines[1], lines[2]

# ダミー result データ作成
result_data = [
    {'user_ID': 1, 'date': 20250624, 'category': 1, 'result': 'win', 'change_coin': 50, 'current_coin': 150},
    {'user_ID': 2, 'date': 20250624, 'category': 2, 'result': 'lose', 'change_coin': -30, 'current_coin': 170},
    {'user_ID': 3, 'date': 20250624, 'category': 1, 'result': 'win', 'change_coin': 40, 'current_coin': 190},
]
df_result = pd.DataFrame(result_data)

# CSV 出力
df_result.to_csv('user_result.csv', index=False)
print("user_result.csv を出力しました。")

# DB 接続
conn = mysql.connector.connect(
    host=host, user=user, password=password, database='user_info'
)
cursor = conn.cursor()

# データ挿入
for _, row in df_result.iterrows():
    table_name = f"user_result_{row['user_ID']}"
    sql = f"""
        INSERT INTO {table_name}
        (user_ID, date, category, result, change_coin, current_coin)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        row['user_ID'], row['date'], row['category'],
        row['result'], row['change_coin'], row['current_coin']
    ))
conn.commit()
print("user_result_xx テーブルへのデータ挿入完了。")

cursor.close()
conn.close()
