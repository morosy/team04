import pandas as pd
import mysql.connector

# アクセス情報を access.txt から読み取り
with open('access.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
host, user, password = lines[0], lines[1], lines[2]

# ダミーユーザデータ作成
data = [
    {'user_name': 'Alice', 'password': 'pass1234', 'current_coin': 100, 'login_count': 1},
    {'user_name': 'Bob', 'password': 'pass5678', 'current_coin': 200, 'login_count': 2},
    {'user_name': 'Charlie', 'password': 'pass9101', 'current_coin': 150, 'login_count': 3},
]
df = pd.DataFrame(data)

# CSV 出力
df.to_csv('user_info.csv', index=False)
print("user_info.csv を出力しました。")

# DB 接続
conn = mysql.connector.connect(
    host=host, user=user, password=password, database='user_info'
)
cursor = conn.cursor()

# CSV 挿入
for _, row in df.iterrows():
    sql = """
        INSERT INTO users (user_name, password, current_coin, login_count)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (row['user_name'], row['password'], row['current_coin'], row['login_count']))
conn.commit()

# 挿入後のユーザーID確認
cursor.execute("SELECT user_ID, user_name FROM users")
users = cursor.fetchall()
for u in users:
    print(f"user_ID: {u[0]}, user_name: {u[1]}")

# ストアド発火
for uid, uname in users:
    cursor.callproc('create_user_result_table', (uid, uname))
print("user_result_xx テーブル作成完了。")

cursor.close()
conn.close()
