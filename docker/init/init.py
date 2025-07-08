# initialization.py
import init_users
import init_user_result
import init_horse_status
import time

def initialize_all():
    print("=== 待機中 ===")
    time.sleep(5)

    print("=== 馬データ挿入中 ===")
    init_horse_status.initialize_horse_status()
    print("=== 馬データ挿入完了 ===")

    print("=== ユーザー挿入中 ===")
    init_users.insert_users()
    print("=== ユーザー挿入完了 ===")

    print("=== 待機中 ===")
    time.sleep(5)

    print("=== ユーザー結果挿入中 ===")
    init_user_result.insert_from_csv()
    print("=== ユーザー結果挿入完了 ===")



if __name__ == "__main__":
    initialize_all()
