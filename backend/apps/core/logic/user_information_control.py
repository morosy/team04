from django.db import connections, transaction
import time

# M1 ユーザデータ送信処理
def userdata_transfer_process(user_id):
    if not userdata_exists(user_id):
        raise ValueError("指定されたユーザが存在しません")
    pass

# M2 フレンド申請済みユーザ送信処理
def already_received_friend_request_user_transfer_process(user_id):
    start = time.time()
    try:
        with connections['friend_db'].cursor() as cursor:
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
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id=%s", [user_id])
        count = cursor.fetchone()[0]
    return count > 0

# --- フレンド申請をDBに登録 ---
def insert_friend_request(from_user_id, to_user_id):
    with transaction.atomic(using='friend_db'):
        with connections['friend_db'].cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM friend_requests WHERE from_user_id=%s AND to_user_id=%s",
                [from_user_id, to_user_id]
            )
            if cursor.fetchone()[0] > 0:
                return False  # 既に申請済み

            if from_user_id == to_user_id:
                return False

            cursor.execute(
                "INSERT INTO friend_requests (from_user_id, to_user_id, status, request_timestamp) VALUES (%s, %s, 'pending', NOW())",
                [from_user_id, to_user_id]
            )
    return True
