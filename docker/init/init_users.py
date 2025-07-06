# init_users.py
import mysql.connector
import random

# DB接続情報（Docker用：hostはサービス名）
db_config = {
    "host": "db",  # ← Docker Compose でのサービス名（例：db）
    "port": 3306,  # コンテナ内は通常3306で接続
    "user": "team04",
    "password": "advinfteam04",
    "database": "user_info"
}

test_users = [
    ("testuser1", "password1"),
    ("testuser2", "password2"),
    ("testuser3", "password3"),
    ("testuser4", "password4"),
    ("testuser5", "password5"),
]

def insert_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for name, pwd in test_users:
            current_coin = random.randint(0, 1000)
            number_of_wins = random.randint(0, 20)
            number_of_losses = random.randint(0, 20)

            insert_sql = """
                INSERT INTO users (user_name, password, current_coin, number_of_wins, number_of_losses)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (name, pwd, current_coin, number_of_wins, number_of_losses))
            conn.commit()

            user_id = cursor.lastrowid
            cursor.callproc("create_user_result_table", [user_id, name])
            conn.commit()

            print(f"User '{name}' inserted with ID {user_id}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    insert_users()
