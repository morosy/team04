from django.shortcuts import render
from .logic.ranking_process import ranking_main_process
from .logic.user_information_process import (
    friend_request_process,
    friend_request_accept_process,
    friend_request_decline_process,
)
from django.db import connections
from django.db import connection
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

'''
def home(request):
    return render(request, 'core/home.html')
'''

'''
    data: 2025/06/23
    カレントディレクトリをfrontendに変更
'''
def home(request):
    return ranking_view(request) #他の機能と結合するときはルーティングを変える


#def ranking_view(request):
#    if request.method == 'POST':
#        result = ranking_main_process(request.POST)
#        return render(request, 'core/ranking.html', {'user_list': result})
#    return render(request, 'core/ranking.html')

def friend_registration_view(request):
    return render(request, 'core/friend-registration.html')

@csrf_exempt
def friend_accept_view(request):
    current_user_id = 1  # ログインユーザーの仮ID--------------------------------------

    if request.method == 'POST':
        selected_ids = request.POST.getlist("selected_applications")
        action = request.POST.get("action")

        for from_user_id in selected_ids:
            if action == "accept":
                friend_request_accept_process(int(from_user_id), current_user_id)
            elif action == "reject":
                friend_request_decline_process(int(from_user_id), current_user_id)

    # GETでもPOSTでも一覧を更新して表示
    applications = []
    with connections['friend_db'].cursor() as cursor:
        cursor.execute("SELECT from_user_id FROM friend_requests WHERE to_user_id=%s", [current_user_id])
        rows = cursor.fetchall()

        for row in rows:
            from_user_id = row[0]
            # user_nameの取得（user_info DB）
            with connections['default'].cursor() as user_cursor:
                user_cursor.execute("SELECT user_name FROM users WHERE user_id = %s", [from_user_id])
                name_row = user_cursor.fetchone()
                player_name = name_row[0] if name_row else "不明なユーザー"
            applications.append({
                'id': from_user_id,
                'player_name': player_name,
            })

    return render(request, 'core/friend-accept.html', {
        'applications': applications
    })

def friend_request_view(request):
    current_user_id = 1  # ログインユーザーIDの仮置き--------------------------------------
    if request.method == 'POST':
        to_user_id = request.POST.get("user_id")
        msg = friend_request_process(current_user_id, int(to_user_id))
        # メッセージとリダイレクトURLをテンプレートに渡す
        redirect_url = reverse('friend_registration')  # ここはフレンド新規登録画面のURL名に変更してください
        return render(request, 'core/friend-request.html', {
            'message': msg,
            'redirect_url': redirect_url,
            'redirect_delay': 2000,  # 3秒後にリダイレクト
        })
    return render(request, 'core/friend-request.html')

def friend_decline_view(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist("check_box")
        msg = friend_request_decline_process(user_ids)
        return render(request, 'core/friend-accept.html', {'message': msg})
    return render(request, 'core/friend-accept.html')

def ranking_view(request):
    current_user_id = 1  # ログイン中のユーザーID（仮）----------------------------------------------------

    if request.method == 'POST':
        post_data = request.POST
    else:
        from django.http import QueryDict
        post_data = QueryDict('', mutable=True)
        post_data.update({
            'coin_button': 'true',
            'win_rate_button': 'false',
            'num_of_win_button': 'false',
            'friend_or_all_button': 'false',
        })

    # フラグの取得（テンプレートで使うため）
    coin = post_data.get('coin_button') == 'true'
    win_rate = post_data.get('win_rate_button') == 'true'
    num_win = post_data.get('num_of_win_button') == 'true'
    is_friend = post_data.get('friend_or_all_button') == 'true'

    user_ids = ranking_main_process(post_data, current_user_id)

    player_list = []
    with connection.cursor() as cursor:
        for idx, user_id in enumerate(user_ids):
            cursor.execute(
                "SELECT user_name, current_coin, "
                "ROUND(CASE WHEN number_of_wins + number_of_losses = 0 THEN 0 ELSE number_of_wins * 100 / (number_of_wins + number_of_losses) END), number_of_wins "
                "FROM user_info.users WHERE user_ID = %s", [user_id]
            )
            row = cursor.fetchone()
            if row:
                player_list.append({
                    'rank': idx + 1,
                    'playerName': row[0],
                    'coin': row[1],
                    'winrate': f"{row[2]}%",
                    'wins': row[3],
                })

    return render(request, 'core/ranking.html', {
        'player_list': player_list,
        'coin': coin,
        'win_rate': win_rate,
        'num_win': num_win,
        'is_friend': is_friend,
    })



'''
    Function Name: user_result_view
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/23
    Description:
        ユーザーの結果を表示するビュー関数.
        ユーザーIDに基づいて、対応するテーブルからデータを取得し、HTMLテンプレートに渡す.
    Parameters: request: HTTPリクエストオブジェクト, user_id: ユーザーID
                user_id: ユーザーID
    Returns: render: ユーザーの結果を表示するHTMLテンプレート
    例外処理: データベース接続やクエリ実行時のエラーをキャッチし、エラーメッセージを表示する.
    例外:
        - データベース接続エラー
        - クエリ実行エラー
    Usage: user_result_view(request, user_id)
'''
def user_result_view(request, user_id):
    table_name = f"user_result_{user_id}"
    query = f"SELECT * FROM `{table_name}` ORDER BY date DESC LIMIT 100;"
    rows = []
    columns = []
    error = None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
    except Exception as e:
        error = str(e)

    return render(request, 'user_result.html', {
        'columns': columns,
        'rows': rows,
        'error': error,
    })
