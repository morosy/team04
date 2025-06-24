from django.db import connection
import time

# M1 ユーザデータ送信処理
def userdata_transfer_process(user_id):
    # 実際のDB連携処理例（登録や更新など）
    # 今回は単純な存在確認のみ例示
    if not userdata_exists(user_id):
        raise ValueError("指定されたユーザが存在しません")
    # 送信処理例（具体的にはDB更新等）
    pass

# M2 フレンド申請済みユーザ送信処理
def already_received_friend_request_user_transfer_process(user_id):
    start = time.time()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT requester_id FROM friend_requests WHERE receiver_id=%s", [user_id])
            rows = cursor.fetchall()
        if time.time() - start > 3:
            raise TimeoutError("ユーザ情報取得がタイムアウトしました")
        friend_request_list = [row[0] for row in rows]
        return friend_request_list
    except Exception as e:
        raise RuntimeError("ユーザ情報を取得できませんでした") from e

# ユーザ存在確認
def userdata_exists(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id=%s", [user_id])
        count = cursor.fetchone()[0]
    return count > 0
