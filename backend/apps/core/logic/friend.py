def friend_request_process(user_id):
    return f"ユーザ {user_id} にフレンド申請を送りました。"

def friend_request_accept_process(user_ids):
    return f"{len(user_ids)}件のフレンド申請を受理しました。"

def friend_request_decline_process(user_ids):
    return f"{len(user_ids)}件のフレンド申請を拒否しました。"

def query_userdata_process():
    # ユーザ情報を取得（ダミー）
    return [], []

def sort_process(data_list, friend_list, coin, win_rate, num_win, is_friend):
    # ソート処理（仮）
    return sorted(data_list)
