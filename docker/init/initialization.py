# initialization.py
import init_users
import init_user_result
import time

def initialize_all():
    print("=== 待機中 ===")
    time.sleep(5)
    print("=== ユーザー挿入中 ===")
    init_users.insert_users()

    print("=== 挿入完了 ===")
    print("=== 待機中 ===")
    time.sleep(5)

    print("=== ユーザー結果挿入中 ===")
    init_user_result.insert_from_csv()

if __name__ == "__main__":
    initialize_all()
