'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/02
    Description:
        user_info データベースの users テーブルのデータをすべて削除するスクリプト。
        テーブル自体は削除せず、全レコードを削除する。
'''

import mysql.connector

# DB接続情報
db_config = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "team04",
    "password": "advinfteam04",
    "database": "user_info"
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # login_attempt_history のデータを削除（users より先）
    cursor.execute("DELETE FROM login_attempt_history;")
    conn.commit()

    # users テーブルのデータを削除
    cursor.execute("DELETE FROM users;")
    conn.commit()

    print("users および login_attempt_history テーブルのデータを削除しました。")

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")