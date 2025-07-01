'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/02
    Description:
        user_info データベースの users テーブルの内容を一覧表示するスクリプト
'''

import mysql.connector
from tabulate import tabulate  # pip install tabulate


def view_users():
    # access.txt から接続情報を読み込み
    with open('access.txt', 'r', encoding='utf-8') as f:
        host = f.readline().strip()
        user = f.readline().strip()
        password = f.readline().strip()

    # MySQL に接続（ポート指定を忘れずに）
    conn = mysql.connector.connect(
        host=host,
        port=3307,
        user=user,
        password=password,
        database='user_info'
    )
    cursor = conn.cursor()

    # users テーブルから全件取得
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # 表形式で表示
    print(tabulate(rows, headers=columns, tablefmt="grid"))

    cursor.close()
    conn.close()


if __name__ == '__main__':
    view_users()
