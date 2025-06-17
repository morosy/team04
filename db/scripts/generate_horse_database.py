'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description: 馬データを生成するスクリプト
'''


import csv
import random
import csv
import mysql.connector


'''
    Function Name: generate_horse_database
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description:
        以下のような規則性に従ったランダムな馬データを生成し, CSVファイルに書き出す
        規則性
        - speed : sprint_status → 高いほど高くなる
        - power : dirt_status → 高いほど高くなる
        - stamina : long_status → 高いほど高くなる
    Parameters:
        N (int): 生成する馬データの件数
    Returns: なし
    Usage: generate_horse_database(N)
'''
def generate_horse_database(N):
    columns = [
        'body_weight', 'power', 'speed', 'stamina',
        'clear_weather_status', 'light_rain_status', 'heavy_rain_status',
        'grass_status', 'dirt_status',
        'sprint_status', 'middle_status', 'long_status'
    ]

    data = []
    for _ in range(N):
        # 馬の体重(kg) JRAの範囲に基づく
        # 体重は400〜550kgの範囲でランダムに生成
        body_weight = random.randint(400, 550)

        # ベースステータス(30〜100)
        power = random.randint(30, 100)
        speed = random.randint(30, 100)
        stamina = random.randint(30, 100)

        # 規則性に基づくステータス(±10でばらつかせるが範囲保証)
        sprint_status = max(30, min(100, speed + random.randint(-10, 10)))
        dirt_status = max(30, min(100, power + random.randint(-10, 10)))
        long_status = max(30, min(100, stamina + random.randint(-10, 10)))

        # 他のステータス(ランダム：30〜100)
        clear_weather_status = random.randint(30, 100)
        light_rain_status = random.randint(30, 100)
        heavy_rain_status = random.randint(30, 100)
        grass_status = random.randint(30, 100)
        middle_status = random.randint(30, 100)

        row = {
            'body_weight': body_weight,
            'power': power,
            'speed': speed,
            'stamina': stamina,
            'clear_weather_status': clear_weather_status,
            'light_rain_status': light_rain_status,
            'heavy_rain_status': heavy_rain_status,
            'grass_status': grass_status,
            'dirt_status': dirt_status,
            'sprint_status': sprint_status,
            'middle_status': middle_status,
            'long_status': long_status
        }

        data.append(row)

    # CSVファイルに書き出し(上書き)
    with open('horse_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

    # Debug
    # print(f"horse_data.csv にリアルなランダムデータ {N} 件を書き出しました")




'''
    Function Name: insert_horse_database
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description:
        horse_data.csv からデータを読み込み、horse_stats テーブルに挿入する
        アクセスするデータベースのIPアドレス、ユーザー名、パスワードは以下のような形式のaccess.txt から読み込む.
        ``` access.txt
        [IPアドレス]
        [ユーザー名]
        [パスワード]
        ```
    Parameters: なし
    Returns: なし
    Usage: insert_horse_database()
'''
def insert_horse_database():
    # access.txtから接続情報を読み込む
    with open('access.txt', 'r', encoding='utf-8') as f:
        host = f.readline().strip()
        user = f.readline().strip()
        password = f.readline().strip()

    # MySQLに接続（horse_dataデータベース）
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='horse_data'
    )
    cursor = conn.cursor()

    # CSVからデータを挿入
    with open('horse_data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = """
                INSERT INTO horse_stats (
                    body_weight, power, speed, stamina,
                    clear_weather_status, light_rain_status, heavy_rain_status,
                    grass_status, dirt_status,
                    sprint_status, middle_status, long_status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = tuple(int(row[col].strip()) for col in reader.fieldnames)
            cursor.execute(query, data)

    # コミットして接続を閉じる
    # データベースに変更を保存
    conn.commit()
    cursor.close()
    conn.close()

    # Debug
    # print("horse_stats にデータ挿入が完了しました")


# if __name__ == '__main__':
#     N = int(100)  # 生成件数
#     generate_horse_database(N)
