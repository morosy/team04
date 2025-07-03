import mysql.connector
import random
from datetime import datetime, timedelta
import csv

# DB接続情報（Docker用）
db_config = {
    "host": "db",
    "port": 3306,
    "user": "team04",
    "password": "advinfteam04",
    "database": "user_info"
}

def insert_user_result(user_id: int, num_records=10):
    """
    指定ユーザーIDの user_result_[ID] テーブルにレコードを挿入（date, category の組み合わせが一意）。
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        table_name = f"user_result_{user_id}"
        base_date = datetime.now().date()
        used_keys = set()
        insert_count = 0
        attempts = 0
        max_attempts = num_records * 10  # 無限ループ防止

        while insert_count < num_records and attempts < max_attempts:
            attempts += 1
            delta_days = random.randint(0, 30)
            date = int((base_date - timedelta(days=delta_days)).strftime("%Y%m%d"))
            category = random.choice([0, 1, 2])
            key = (date, category)

            if key in used_keys:
                continue  # 重複はスキップ

            used_keys.add(key)

            result = random.choice(["win", "lose"])
            coin_change = random.randint(50, 200)
            change_coin = coin_change if result == "win" else -coin_change
            current_coin = random.randint(0, 1000)

            insert_sql = f"""
                INSERT INTO {table_name} (user_ID, date, category, result, change_coin, current_coin)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (user_id, date, category, result, change_coin, current_coin))
            insert_count += 1

        conn.commit()
        cursor.close()
        conn.close()

        print(f"user_ID={user_id} に {insert_count} 件のデータを挿入しました。")

    except mysql.connector.Error as err:
        print(f"user_ID={user_id} エラー: {err}")

def insert_from_csv(csv_path="init.csv"):
    """
    init.csv を読み込んで user_ID と件数を取得して処理を実行。
    """
    try:
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = int(row["ID"])
                num = int(row["number"])
                insert_user_result(user_id, num)
    except FileNotFoundError:
        print(f"CSVファイル {csv_path} が見つかりません。")
    except Exception as e:
        print(f"CSV読み込み中のエラー: {e}")

if __name__ == "__main__":
    insert_from_csv()
