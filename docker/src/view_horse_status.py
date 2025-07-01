'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/02
    Description:
        horse_data データベースの horse_status テーブルの中身を
        標準出力および output.txt に出力するスクリプト
'''

import mysql.connector
from tabulate import tabulate

# 接続情報
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "team04",
    "password": "advinfteam04",
    "database": "horse_data"
}

def view_horse_status():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM horse_status;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if not rows:
            output = "horse_status テーブルは空です。"
        else:
            output = tabulate(rows, headers=columns, tablefmt="grid")

        # ターミナルに出力
        print(output)

        # ファイルに出力
        with open("../logs/output_horse_status.log", "w", encoding="utf-8") as f:
            f.write(output + "\n")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        with open("../logs/output_horse_status.log", "w", encoding="utf-8") as f:
            f.write(f"Error: {err}\n")


if __name__ == "__main__":
    view_horse_status()
