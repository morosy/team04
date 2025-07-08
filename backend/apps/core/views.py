# feature/ranking-friend
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
from django.db import connection
from django.contrib.auth.views import LogoutView

from django.shortcuts import render
from django.shortcuts import redirect
from new_registration.register_name.models import UserCredentials
from django.contrib import messages

from keiba_auth.login_request.views import Userdata_reader
import MySQLdb
from collections import namedtuple
from datetime import datetime
import random
from .models import HorseStats
from apps.core.models import User


from django.views.decorators.csrf import csrf_exempt


'''
def home(request):
    return render(request, 'core/home.html')
'''

'''
    data: 2025/06/23
    change: 2025/07/03
    Designer: Shunsuke MOROZUMI
    Description:
        ユーザーのホームページを表示するビュー関数.
        ユーザーIDをセッションから取得し、ユーザー情報をデータベースから取得して、
        HTMLテンプレートに渡す.
    Parameters: request: HTTPリクエストオブジェクト
    Returns: render: ユーザーのホームページを表示するHTMLテンプレート
    Usage: home_view(request)
'''
def home(request):
    user_id = request.session.get('logged_in_user_id')
    if not user_id:
        return redirect('login_form')

    user, success = Userdata_reader(user_id)
    if not success:
        return redirect('login_form')

    return render(request, 'home.html', {
        'user_id': user.user_id,
        'user_name': user.user_name,
        'current_coin': user.current_coin or 0,
    })
    # return ranking_view(request) #他の機能と結合するときはルーティングを変える


#def ranking_view(request):
#    if request.method == 'POST':
#        result = ranking_main_process(request.POST)
#        return render(request, 'core/ranking.html', {'user_list': result})
#    return render(request, 'core/ranking.html')

def friend_registration_view(request):
    return render(request, 'friend-registration.html')

@csrf_exempt
def friend_accept_view(request):
    current_user_id = request.session.get('logged_in_user_id')

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

    return render(request, 'friend-accept.html', {
        'applications': applications
    })

def friend_request_view(request):
    current_user_id = request.session.get('logged_in_user_id')
    if request.method == 'POST':
        to_user_id = request.POST.get("user_id")
        msg = friend_request_process(current_user_id, int(to_user_id))
        # メッセージとリダイレクトURLをテンプレートに渡す
        redirect_url = reverse('friend_registration')  # ここはフレンド新規登録画面のURL名に変更してください
        return render(request, 'friend-request.html', {
            'message': msg,
            'redirect_url': redirect_url,
            'redirect_delay': 2000,  # 3秒後にリダイレクト
        })
    return render(request, 'friend-request.html')


def friend_decline_view(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist("check_box")
        msg = friend_request_decline_process(user_ids)
        return render(request, 'friend-accept.html', {'message': msg})
    return render(request, 'friend-accept.html')


def ranking_view(request):
    current_user_id = request.session.get('logged_in_user_id')

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

    return render(request, 'ranking.html', {
        'player_list': player_list,
        'coin': coin,
        'win_rate': win_rate,
        'num_win': num_win,
        'is_friend': is_friend,
    })



'''
    Function Name: user_result
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/23
    Change: 2025/07/03
    Description:
        ユーザーの結果を表示するビュー関数.
        ユーザーIDをURLパラメータから取得し、対応するテーブルからデータを取得して、
        HTMLテンプレートに渡す.
    Parameters: request: HTTPリクエストオブジェクト, user_id: ユーザーID
    Returns: render: ユーザーの結果を表示するHTMLテンプレート
    Usage: user_result(request, user_id)
'''
def user_result(request, user_id):
    # ユーザー名取得
    try:
        user = UserCredentials.objects.get(user_id=user_id)
        user_name = user.user_name
    except UserCredentials.DoesNotExist:
        user_name = "不明なユーザー"

    # DB接続して結果取得
    conn = MySQLdb.connect(
        host='db',
        user='team04',
        passwd='advinfteam04',
        db='user_info',
        charset='utf8'
    )
    cursor = conn.cursor()
    try:
        query = f"""
            SELECT date, category, result, change_coin, current_coin 
            FROM user_result_{user_id}
            ORDER BY date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        rows = []
    finally:
        conn.close()

    # 整形
    ResultRow = namedtuple("ResultRow", ["date", "category", "result", "coin_change", "total_coin"])
    result_rows = [
        ResultRow(
            date=datetime.strptime(str(row[0]), "%Y%m%d"),
            category=row[1],
            result="1着" if row[2] == "win" else "ハズレ",
            coin_change=row[3],
            total_coin=row[4]
        )
        for row in rows
    ]

    return render(request, "user_result.html", {
        "user_ID": f"{int(user_id):08d}",  # 8桁ゼロ埋め
        "user_name": user_name,
        "result_rows": result_rows
    })



'''
    Function Name: mypage
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/29
    Change: 2025/07/03
    Description:
        マイページを表示するビュー関数.
        ユーザーIDとユーザー名をセッションから取得し、HTMLテンプレートに渡す.
        ユーザーIDは8桁のゼロ埋め形式で表示する.
    Parameters: request: HTTPリクエストオブジェクト
    Returns: render: マイページを表示するHTMLテンプレート
    Usage: mypage(request)
'''
def mypage(request):
    user_id = request.session.get('logged_in_user_id')
    user_name = request.session.get('logged_in_user_name')

    if not user_id or not user_name:
        return redirect('login_form')

    formatted_user_id = f"{int(user_id):08d}"

    context = {
        'user_ID': formatted_user_id,
        'user_name': user_name,
    }

    return render(request, 'mypage.html', context)


'''
    Function Name: update_username
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/08
    Description:
        ユーザー名を更新するためのビュー関数.
    Parameters: request: HTTPリクエストオブジェクト
    Returns: redirect: マイページへのリダイレクト
    Usage: update_username(request)
'''
@csrf_exempt
def update_username(request):
    if request.method == "POST":
        user_id = request.POST.get("user_ID")
        new_username = request.POST.get("new_username")

        try:
            user = UserCredentials.objects.get(user_id=user_id)
            user.user_name = new_username
            user.save()

            # セッション内のユーザー名も更新
            request.session['logged_in_user_name'] = new_username

            return redirect('mypage')
        except UserCredentials.DoesNotExist:
            return render(request, "error.html", {"message": "ユーザーが存在しません。"})

    return redirect('home')



'''
    Class Name: LogoutViewAllowGet
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/03
    Description:
        ログアウトビューをGETリクエストでも許可するためのクラス
        基本的に使わない
'''
# class LogoutViewAllowGet(LogoutView):
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


'''
    Function Name: select_ticket
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/03
    Description:
        馬券選択画面を表示するビュー関数.
        ユーザーIDをセッションから取得し、HTMLテンプレートに渡す.
        ユーザーIDが存在しない場合はログイン画面へリダイレクトする.
    Parameters: request: HTTPリクエストオブジェクト
    Returns: render: 馬券選択画面を表示するHTMLテンプレート
    Usage: select_ticket(request)
'''
def select_ticket(request):
    user_id = request.session.get('logged_in_user_id')

    if user_id is None:
        return redirect('login')  # 未ログインならログインへ

    try:
        user = UserCredentials.objects.get(user_id=user_id)
    except UserCredentials.DoesNotExist:
        return redirect('login')

    context = {
        'user_ID': f"{int(user.user_id):08d}",  # ゼロ埋め表示
        'user_name': user.user_name,
        'current_coin': user.current_coin,
    }
    return render(request, 'select_ticket.html', context)



def race1(request):
    # セッションに user_id があるか確認
    user_id = request.session.get('logged_in_user_id')
    if not user_id:
        return redirect('login')  # 未ログインならログインページへ

    try:
        # user_id から User オブジェクトを取得
        user = UserCredentials.objects.get(user_id=user_id)
    except UserCredentials.DoesNotExist:
        return redirect('login')  # 不正な ID の場合もログインへ

    # コイン枚数
    current_coin = user.current_coin

    # 天気・トラック・距離をランダムに決定
    weather = random.choice(['晴れ', '小雨', '大雨'])
    track = random.choice(['芝', 'ダート'])
    distance = random.choice(range(1000, 3100, 100))  # 1000〜3000の100刻み

    # horse_data DB からランダムに6頭取得
    horses = HorseStats.objects.using('horse_data').order_by('?')[:6]

    # ランダムオッズ（馬ごとに1.2〜9.9の範囲で生成）
    odds_list = [round(random.uniform(1.2, 9.9), 1) for _ in range(6)]
    horse_info = list(zip(range(1, 7), horses, odds_list))  # (馬番号, horse, オッズ)

    context = {
        'user_ID': str(user.user_id).zfill(8),
        'user_name': user.user_name,
        'current_coin': current_coin,
        'weather': weather,
        'track': track,
        'distance': distance,
        'horse_info': horse_info,  # テンプレートで馬名とオッズを表示
    }

    return render(request, 'race1.html', context)

