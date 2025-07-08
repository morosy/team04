'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/02
    Description: Dockerのhorse_dataデータベース内 horse_status テーブルを削除→生成→挿入するスクリプト
'''

import mysql.connector
import random
import datetime
import os


# 接続情報（Docker用）
DB_CONFIG = {
    "host": "db",  # Dockerネットワーク内のMySQLコンテナ名
    "port": 3306,
    "user": "team04",
    "password": "advinfteam04",
    "database": "horse_data"
}



def write_log(message: str):
    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)  # ここでディレクトリ作成

    jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')
    now = datetime.datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S %Z")
    log_path = os.path.join(log_dir, "log_horse_status.log")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")


def delete_horse_status():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE horse_status;")
    conn.commit()
    cursor.close()
    conn.close()
    write_log("horse_status テーブルのデータを削除しました")


def generate_horse_data(N):
    data = []
    for _ in range(N):
        body_weight = random.randint(400, 550)
        power = random.randint(30, 100)
        speed = random.randint(30, 100)
        stamina = random.randint(30, 100)

        sprint_status = max(30, min(100, speed + random.randint(-10, 10)))
        dirt_status = max(30, min(100, power + random.randint(-10, 10)))
        long_status = max(30, min(100, stamina + random.randint(-10, 10)))

        clear_weather_status = random.randint(30, 100)
        light_rain_status = random.randint(30, 100)
        heavy_rain_status = random.randint(30, 100)
        grass_status = random.randint(30, 100)
        middle_status = random.randint(30, 100)

        row = (
            body_weight, power, speed, stamina,
            clear_weather_status, light_rain_status, heavy_rain_status,
            grass_status, dirt_status, sprint_status, middle_status, long_status
        )
        data.append(row)
    return data


def insert_horse_status(data):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    insert_sql = """
        INSERT INTO horse_status (
            body_weight, power, speed, stamina,
            clear_weather_status, light_rain_status, heavy_rain_status,
            grass_status, dirt_status,
            sprint_status, middle_status, long_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for row in data:
        cursor.execute(insert_sql, row)
    conn.commit()
    cursor.close()
    conn.close()
    write_log(f"horse_status テーブルに {len(data)} 件のデータを挿入しました")


def initialize_horse_status(N=100):
    try:
        write_log("=== horse_status 更新処理 開始 ===")
        delete_horse_status()
        horse_data = generate_horse_data(N)
        write_log(f"{N} 件のデータを生成しました")
        insert_horse_status(horse_data)
        write_log("=== horse_status 更新処理 正常終了 ===")
    except Exception as e:
        write_log(f"エラー発生: {str(e)}")


# CLI実行用
if __name__ == "__main__":
    initialize_horse_status()
