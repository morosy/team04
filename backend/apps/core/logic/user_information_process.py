from .user_information_control import (
    userdata_exists,
    userdata_transfer_process,
    insert_friend_request,
)
from django.db import connections, transaction

# M4 フレンド申請処理
def friend_request_process(from_user_id, to_user_id):
    if not userdata_exists(to_user_id):
        raise ValueError("申請先ユーザが存在しません")

    success = insert_friend_request(from_user_id, to_user_id)
    if not success:
        return "すでに申請済み、または無効な申請です。"
    return f"ユーザ {to_user_id} にフレンド申請を送りました。"


# M5 フレンド申請受け入れ処理
def friend_request_accept_process(from_user_id, to_user_id):
    if not userdata_exists(to_user_id):
        raise ValueError("ユーザが存在しません")

    accept_friend_request(from_user_id, to_user_id)
    return "フレンド申請を受け入れました。"

# M6 フレンド登録処理
def friend_register_process(user_id):
    # C6モジュールの処理呼び出し（仮）
    userdata_transfer_process(user_id)
    # ここでDBへの友達登録処理を行う想定
    return f"ユーザ {user_id} をフレンド登録しました。"

# M7 フレンド申請拒否処理
def friend_request_decline_process(from_user_id, to_user_id):
    if not userdata_exists(to_user_id):
        raise ValueError("ユーザが存在しません")

    decline_friend_request(from_user_id, to_user_id)
    return "フレンド申請を拒否しました。"

# --- フレンド申請を受け入れる（友達登録）---
def accept_friend_request(from_user_id, to_user_id):
    with transaction.atomic(using='friend_db'):
        with connections['friend_db'].cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM friends WHERE user_id=%s AND friend_id=%s",
                [from_user_id, to_user_id]
            )
            exists = cursor.fetchone()[0]
            if exists == 0:
                cursor.execute(
                    "INSERT INTO friends (user_id, friend_id, created_at) VALUES (%s, %s, NOW())",
                    [from_user_id, to_user_id]
                )
            cursor.execute(
                "SELECT COUNT(*) FROM friends WHERE user_id=%s AND friend_id=%s",
                [to_user_id, from_user_id]
            )
            exists = cursor.fetchone()[0]
            if exists == 0:
                cursor.execute(
                    "INSERT INTO friends (user_id, friend_id, created_at) VALUES (%s, %s, NOW())",
                    [to_user_id, from_user_id]
                )

            cursor.execute(
                "DELETE FROM friend_requests WHERE from_user_id=%s AND to_user_id=%s",
                [from_user_id, to_user_id]
            )
    return True

# --- フレンド申請を拒否（申請削除）---
def decline_friend_request(from_user_id, to_user_id):
    with transaction.atomic(using='friend_db'):
        with connections['friend_db'].cursor() as cursor:
            cursor.execute(
                "DELETE FROM friend_requests WHERE from_user_id=%s AND to_user_id=%s",
                [from_user_id, to_user_id]
            )
    return True
