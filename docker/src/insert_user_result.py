import mysql.connector
import random
import sys
from datetime import datetime
from datetime import timedelta
import os

# DB接続情報
db_config = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "team04",
    "password": "advinfteam04",
    "database": "user_info"
}

# ログファイルパス
log_path = "../logs/user_result.log"

def log_message(message: str):
    """
    ログファイルにメッセージを追記する関数。
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry)

def generate_user_result_data(user_id, num_records=10):
    """
    指定した user_ID に対応する user_result_[ID] テーブルにランダムなレコードを挿入し、ログに記録する。

    Parameters:
        user_id (int): 対象ユーザーID
        num_records (int): 挿入するレコード数（デフォルトは10）
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        table_name = f"user_result_{user_id}"
        insert_count = 0


        base_date = datetime.now().date()

        for _ in range(num_records):
            # 日付に最大30日のずれを加えることで重複回避
            delta_days = random.randint(0, 30)
            date = int((base_date - timedelta(days=delta_days)).strftime("%Y%m%d"))

            category = random.choice([0, 1, 2])
            result = random.choice(["win", "lose"])
            coin_change_value = random.randint(50, 200)
            change_coin = coin_change_value if result == "win" else -coin_change_value
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

        log_message(f"user_ID={user_id} に {insert_count} 件の結果（勝敗+コイン増減）を挿入しました。")

    except mysql.connector.Error as err:
        error_msg = f"user_ID={user_id} の挿入中にエラー発生: {err}"
        log_message(error_msg)
        print(f"Error: {err}")

# ======================
# メイン処理（コマンドライン実行用）
# ======================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python insert_user_result.py <user_ID> [num_records]")
        sys.exit(1)

    user_id = int(sys.argv[1])
    num_records = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

    generate_user_result_data(user_id, num_records)
