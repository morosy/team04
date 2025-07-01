import mysql.connector
import random

# DB接続情報
db_config = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "team04",
    "password": "advinfteam04",
    "database": "user_info"
}

# テストユーザー情報
test_users = [
    ("testuser1", "pass1"),
    ("testuser2", "pass2"),
    ("testuser3", "pass3"),
    ("testuser4", "pass4"),
    ("testuser5", "pass5"),
]

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    for name, pwd in test_users:
        current_coin = random.randint(0, 1000)
        number_of_wins = random.randint(0, 20)
        number_of_losses = random.randint(0, 20)

        # INSERT実行（勝ち数・負け数も含む）
        insert_sql = """
            INSERT INTO users (user_name, password, current_coin, number_of_wins, number_of_losses)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (name, pwd, current_coin, number_of_wins, number_of_losses))
        conn.commit()

        # 挿入したuser_IDを取得
        user_id = cursor.lastrowid

        # ストアドプロシージャ呼び出し
        cursor.callproc("create_user_result_table", [user_id, name])
        conn.commit()

        print(f"User '{name}' inserted with ID {user_id}, coin={current_coin}, wins={number_of_wins}, losses={number_of_losses}, and result table created.")

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
