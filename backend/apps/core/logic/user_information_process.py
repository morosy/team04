from .user_information_control import userdata_exists, userdata_transfer_process

# M4 フレンド申請処理
def friend_request_process(user_id):
    if not userdata_exists(user_id):
        raise ValueError("指定されたユーザが存在しません")
    # C6のユーザ情報管理部に送信（仮）
    userdata_transfer_process(user_id)
    return f"ユーザ {user_id} にフレンド申請を送りました。"

# M5 フレンド申請受け入れ処理
def friend_request_accept_process(user_ids):
    for uid in user_ids:
        if not userdata_exists(uid):
            raise ValueError(f"ユーザID {uid} は存在しません")
        friend_register_process(uid)
    return f"{len(user_ids)}件のフレンド申請を受理しました。"

# M6 フレンド登録処理
def friend_register_process(user_id):
    # C6モジュールの処理呼び出し（仮）
    userdata_transfer_process(user_id)
    # ここでDBへの友達登録処理を行う想定
    return f"ユーザ {user_id} をフレンド登録しました。"

# M7 フレンド申請拒否処理
def friend_request_decline_process(user_ids):
    for uid in user_ids:
        if not userdata_exists(uid):
            raise ValueError(f"ユーザID {uid} は存在しません")
        # C6の申請消去処理を呼び出し（仮）
        # 例: userdata_delete_friend_request(user_id)
    return f"{len(user_ids)}件のフレンド申請を拒否しました。"
