from django.shortcuts import render
from .logic.ranking_process import ranking_main_process
from .logic.user_information_process import (
    friend_request_process,
    friend_request_accept_process,
    friend_request_decline_process,
)
from django.db import connection


'''
def home(request):
    return render(request, 'core/home.html')
'''

'''
    data: 2025/06/23
    カレントディレクトリをfrontendに変更
'''
def home(request):
    return render(request, 'core/ranking.html')



def ranking_view(request):
    if request.method == 'POST':
        result = ranking_main_process(request.POST)
        return render(request, 'core/ranking.html', {'user_list': result})
    return render(request, 'core/ranking.html')

def friend_registration_view(request):
    return render(request, 'core/friend-registration.html')

def friend_request_view(request):
    if request.method == 'POST':
        msg = friend_request_process(request.POST.get("user_id"))
        return render(request, 'core/friend-request.html', {'message': msg})
    return render(request, 'core/friend-request.html')

def friend_accept_view(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist("check_box")
        msg = friend_request_accept_process(user_ids)
        return render(request, 'core/friend-acceptance.html', {'message': msg})
    return render(request, 'core/friend-acceptance.html')

def friend_decline_view(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist("check_box")
        msg = friend_request_decline_process(user_ids)
        return render(request, 'core/friend-acceptance.html', {'message': msg})
    return render(request, 'core/friend-acceptance.html')
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
