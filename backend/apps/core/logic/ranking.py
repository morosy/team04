from django.db import connection
import time

# M1 ランキング主処理
def ranking_main_process(post_data):
    coin = post_data.get('coin_button') == 'true'
    win_rate = post_data.get('win_rate_button') == 'true'
    num_win = post_data.get('num_of_win_button') == 'true'
    is_friend = post_data.get('friend_or_all_button') == 'true'

    try:
        data_list, friend_list = query_userdata_process()
    except Exception as e:
        # views側で例外をcatchするためraise
        raise e

    user_list = sort_process(data_list, friend_list, coin, win_rate, num_win, is_friend)
    return user_list

# M2 ユーザデータ問合せ処理
def query_userdata_process():
    start = time.time()
    try:
        with connection.cursor() as cursor:
            # 例: ユーザ情報とフレンド関係を取得するSQL（実際のDB構造に合わせて修正必要）
            cursor.execute("SELECT user_id, coin, wins, win_rate FROM users")
            users = cursor.fetchall()

            cursor.execute("SELECT user_id, friend_user_id FROM friends")
            friends = cursor.fetchall()

        if time.time() - start > 3:
            raise TimeoutError("ユーザ情報取得がタイムアウトしました")

        # data_list: {user_id: [coin, wins, win_rate]}
        data_list = {u[0]: [u[1], u[2], u[3]] for u in users}
        # friend_list: {user_id: [friend_user_id, ...]}
        friend_list = {}
        for u_id, f_id in friends:
            friend_list.setdefault(u_id, []).append(f_id)

        return data_list, friend_list

    except Exception as e:
        raise RuntimeError("ユーザ情報を取得できませんでした") from e

# M3 ソート処理
def sort_process(data_list, friend_list, coin, win_rate, num_win, is_friend):
    # user_listの元データをdata_listのキーから作成
    # friend_listで絞り込みも行う
    # フレンドのみ表示の場合はfriend_listのキーを利用

    # 対象ユーザ絞り込み
    if is_friend:
        # フレンド関係がなければ空リストを返す
        # ここでは例として、全ユーザのフレンドリストから対象ユーザを抽出（実際はログインユーザIDに基づくべき）
        target_users = set()
        for friends in friend_list.values():
            target_users.update(friends)
    else:
        target_users = data_list.keys()

    # フィルタリング後リスト作成
    filtered_users = [user for user in data_list.keys() if user in target_users]

    # ソートキー定義（優先順位に基づく例）
    def sort_key(user):
        coin_val, wins_val, win_rate_val = data_list[user]
        key = ()
        if coin:
            key += (-coin_val,)  # 降順
        if win_rate:
            key += (-win_rate_val,)
        if num_win:
            key += (-wins_val,)
        # 何も押されてなければuser_id順
        if not key:
            key = (user,)
        return key

    user_list = sorted(filtered_users, key=sort_key)
    return user_list
