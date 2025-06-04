import csv
import mysql.connector
from datetime import datetime

# access.txtから接続情報を取得
with open('access.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines()]
    host = lines[0]
    user = lines[1]
    password = lines[2]

# MySQLに接続
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database='user_info'
)
cursor = conn.cursor()

# CSV読み込みとINSERT処理
with open('userinfo_testdata.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # キーの前後の空白を除去して安全にアクセス
        row = {k.strip(): v.strip() for k, v in row.items()}

        timestamp = datetime.now() if row.get('login_timestamp', '').lower() == 'true' else None

        insert_query = """
            INSERT INTO users
            (user_ID, user_name, password, current_coin, login_timestamp, login_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (
            int(row['user_ID']),
            row['user_name'],
            row['password'],
            int(row['current_coin']),
            timestamp,
            int(row['login_count'])
        )
        cursor.execute(insert_query, data)

conn.commit()
cursor.close()
conn.close()
print("CSVデータの挿入が完了しました")
