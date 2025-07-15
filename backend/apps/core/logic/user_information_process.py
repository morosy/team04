#   Designer: Kuraishi Sora
#   Date: 2025/07/15
#   Description: フレンド登録関連の処理を行うpythonファイル
#   Note: このファイルは, フレンド登録のためのデータを受け取り、フレンド登録に必要な処理を行うためのpythonファイル.

from .user_information_control import (
    userdata_exists, userdata_transfer_process,
    insert_friend_request, accept_friend_request, decline_friend_request
)

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
