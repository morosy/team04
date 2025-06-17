'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description: 既存の馬データベースを削除するスクリプト
'''


import mysql.connector


'''
    Function Name: delete_horse_database
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description:
        データベースに保存されている馬データを削除する.
        すべてのテーブルの中身を削除するが、テーブル自体は削除しない.
        アクセスするデータベースのIPアドレス、ユーザー名、パスワードは以下のような形式のaccess.txt から読み込む.
        ``` access.txt
        [IPアドレス]
        [ユーザー名]
        [パスワード]
        ```
    Parameters: なし
    Returns: なし
    Usage: delete_horse_database()
'''
def delete_horse_database():
    # 接続情報の読み込み
    with open('access.txt', 'r', encoding='utf-8') as f:
        host = f.readline().strip()
        user = f.readline().strip()
        password = f.readline().strip()

    # 対象のデータベース名
    target_database = 'horse_data'

    # MySQLに接続
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=target_database
    )
    cursor = conn.cursor()

    # データベース内のテーブル一覧を取得
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    # 各テーブルに対して TRUNCATE を実行
    for (table_name,) in tables:
        print(f"Truncating table: {table_name}")
        cursor.execute(f"TRUNCATE TABLE {table_name};")

    conn.commit()
    cursor.close()
    conn.close()

    # Debug
    # print(f"データベース `{target_database}` 内のすべてのテーブルの中身を削除しました")



# if __name__ == "__main__":
#     delete_horse_database()
