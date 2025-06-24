from django.shortcuts import render
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
    return render(request, 'home.html')



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