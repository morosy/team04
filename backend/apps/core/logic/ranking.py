def ranking_main_process(post_data):
    coin = post_data.get('coin_button') == 'true'
    win_rate = post_data.get('win_rate_button') == 'true'
    num_win = post_data.get('num_of_win_button') == 'true'
    is_friend = post_data.get('friend_or_all_button') == 'true'

    data_list = []  # 例: DBやCSVから取得
    friend_list = []
    # ソート処理（仮）
    user_list = sort_process(data_list, friend_list, coin, win_rate, num_win, is_friend)
    return user_list
