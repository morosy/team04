from django.db import connection
import time
import logging

# M1 ランキング主処理
def ranking_main_process(post_data, current_user_id):
    coin = post_data.get('coin_button') == 'true'
    win_rate = post_data.get('win_rate_button') == 'true'
    num_win = post_data.get('num_of_win_button') == 'true'
    is_friend = post_data.get('friend_or_all_button') == 'true'

    try:
        data_list, friend_list = query_userdata_process()
    except Exception as e:
        raise e

    user_list = sort_process(data_list, friend_list, coin, win_rate, num_win, is_friend, current_user_id)
    return user_list


# M2 ユーザデータ問合せ処理
def query_userdata_process():
    with connection.cursor() as cursor:
        # 明示的にデータベースを指定してSELECT
        cursor.execute("SELECT user_ID, current_coin, number_of_wins, number_of_losses FROM user_info.users;")
        users = cursor.fetchall()

        cursor.execute("SELECT user_id, friend_id FROM friend.friends;")
        friends = cursor.fetchall()


    data_list = {}
    for u in users:
        user_id = u[0]
        coin = u[1]
        wins = u[2]
        losses = u[3]
        win_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
        data_list[user_id] = [coin, wins, win_rate]

    friend_list = {}
    for u_id, f_id in friends:
        friend_list.setdefault(u_id, []).append(f_id)

    return data_list, friend_list



# M3 ソート処理
def sort_process(data_list, friend_list, coin, win_rate, num_win, is_friend, current_user_id):
    if is_friend:
        target_users = set(friend_list.get(current_user_id, []))
    else:
        target_users = set(data_list.keys())

    filtered_users = [user for user in data_list if user in target_users]
    def sort_key(user):
        coin_val, wins_val, win_rate_val = data_list[user]
        key = ()
        if coin:
            key += (-coin_val,)
        if win_rate:
            key += (-win_rate_val,)
        if num_win:
            key += (-wins_val,)
        if not key:
            key = (user,)
        return key

    return sorted(filtered_users, key=sort_key)
