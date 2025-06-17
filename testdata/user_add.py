import mysql.connector

def read_access_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        if len(lines) < 3:
            raise ValueError("access.txt の内容が不足しています。")
        return {
            'host': lines[0],
            'user': lines[1],
            'password': lines[2],
            'database': 'friend'
        }

def main():
    try:
        # access.txt から接続情報読み込み
        config = read_access_file('access.txt')

        # DB接続
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # テスト用 uid
        test_uid = 1

        # ストアドプロシージャ呼び出し
        cursor.callproc('create_friend_table', [test_uid])
        print(f"Procedure create_friend_table({test_uid}) executed.")

        # テーブル作成確認
        table_name = f"friend_user_{test_uid}"
        cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        result = cursor.fetchone()

        if result:
            print(f"Table `{table_name}` successfully created.")
        else:
            print(f"Table `{table_name}` was not created.")

        # テーブルの構造表示
        cursor.execute(f"DESCRIBE {table_name};")
        columns = cursor.fetchall()
        print("Table structure:")
        for column in columns:
            print(column)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    except Exception as ex:
        print(f"Exception: {ex}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()