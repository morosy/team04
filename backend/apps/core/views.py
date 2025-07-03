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


def ranking(request):
    return render(request, 'ranking.html')


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