# backend/keiba_auth/login_request/views.py

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import logging
from django.db import transaction
from django.db import connection
from django.utils.timezone import localdate

import logging

# Djangoの認証関連のインポート
from django.contrib.auth import authenticate, login, logout

# UserCredentials モデルをインポート
from new_registration.register_name.models import UserCredentials
# 今回定義したモデルをインポート
from .models import LoginAttemptHistory

# C4 ユーザー情報管理 - ユーザーデータ呼び出し処理: Userdata_reader に対応
def Userdata_reader(user_identifier):
    try:
        # 生のSQLクエリを使ってユーザーデータを取得
        with connection.cursor() as cursor:
            # users テーブルから必要なカラムを選択
            # カラム名と順序はDBのusersテーブルと完全に一致させてください。
            # user_ID, user_name, password, current_coin, login_timestamp, login_count
            cursor.execute(
                "SELECT user_ID, user_name, password, current_coin, login_timestamp, login_count FROM users WHERE user_ID = %s",
                [user_identifier]
            )
            row = cursor.fetchone() # 1行だけ取得

        if row:
            # UserCredentials モデルのインスタンスを手動で作成し、属性を埋める
            user_obj = UserCredentials()
            user_obj.user_id = row[0]
            user_obj.user_name = row[1] # ここでuser_nameを確実にセット
            user_obj.password = row[2]
            user_obj.current_coin = row[3]
            user_obj.login_timestamp = row[4]
            user_obj.login_count = row[5]

            # ここでデバッグログを出力しても良い
            # logging.error(f"DEBUG: Userdata_reader fetched user_name: {user_obj.user_name}")

            return user_obj, True # 属性が埋められたオブジェクトを返す

        # ユーザーが見つからない場合
        logging.error(f"DEBUG: User ID {user_identifier} not found in UserCredentials table via raw SQL.")
        return None, False
    except Exception as e:
        # データベースエラーやその他の予期せぬエラー
        logging.error(f"DEBUG: Error in Userdata_reader (raw SQL): {str(e)}")
        return None, False

# C5 ユーザー情報管理 - コイン追加処理: coin_addition に対応
def coin_addition(user, coin_amount):
    try:
        user.current_coin = (user.current_coin or 0) + coin_amount
        user.save()
        return True # coin_update_success
    except Exception as e:
        logging.error(f"Coin addition failed for user {user.user_name}: {e}")
        return False

# C5 ユーザー情報管理 - ログイン履歴登録処理: login_update に対応
# ログイン回数を users.login_count に直接記録する場合
def login_update_user_count(user):
    try:
        user.login_count = (user.login_count or 0) + 1
        user.save()
        return True
    except Exception as e:
        logging.error(f"Failed to update login_count for user {user.user_name}: {e}")
        return False

# C2 認証処理部 - ログイン履歴処理: login_count_Main に対応
def login_count_Main(user):
    try:
        with transaction.atomic():
            success_update_count = login_update_user_count(user)
            if not success_update_count:
                return False, user.login_count

            today = timezone.now().date()
            is_first_login_today = not LoginAttemptHistory.objects.filter(
                user=user,
                success=True,
                attempt_timestamp__date=today
            ).exists()

            if is_first_login_today:
                coin_add_success = coin_addition(user, 100)
                if not coin_add_success:
                    logging.error(f"Failed to add coins for first login of user {user.user_name} today.")
                    pass

            return True, user.login_count
    except Exception as e:
        logging.error(f"Error in login_count_Main for user {user.user_name}: {e}")
        return False, user.login_count

def verify_password(raw_password, stored_password):

    return raw_password == stored_password 

# C2 認証処理部 - ログイン要求処理: login_request_Main に対応 (POSTリクエストを処理)
@require_POST
def login_process_view(request):
    user_id = request.POST.get('user_id')
    password = request.POST.get('password')

    if not user_id or not password:
        return JsonResponse({'success': False, 'message': 'ユーザーIDとパスワードを入力してください。'})

    # ユーザーデータ呼び出し処理 (C4)
    user_credentials, found = Userdata_reader(user_id)

    if found:
        if password == user_credentials.password:
            # 認証成功（カスタム認証）
            # request.session にユーザー情報を保存
            request.session['logged_in_user_id'] = user_credentials.user_id
            request.session['logged_in_user_name'] = user_credentials.user_name

            # ログイン履歴、コイン追加などのロジック
            # ここで login_count_Main を呼び出す
            login_success, updated_login_count = login_count_Main(user_credentials)

            LoginAttemptHistory.objects.create(user=user_credentials, success=True)
            return JsonResponse({'success': True, 'redirect_url': '/home/'})
        else:
            # パスワード不一致
            LoginAttemptHistory.objects.create(user=user_credentials, success=False)
            return JsonResponse({'success': False, 'message': 'ユーザーIDまたはパスワードが正しくありません。'})
    else:
        # ユーザーが見つからない
        return JsonResponse({'success': False, 'message': 'ユーザーIDまたはパスワードが正しくありません。'})

# ログアウト機能
def user_logout(request):
    # Django標準のlogout()関数があれば使う
    logout(request) # これでセッションから認証情報がクリアされる
    # セッションからカスタム情報を削除
    if 'logged_in_user_id' in request.session:
        del request.session['logged_in_user_id']
    if 'logged_in_user_name' in request.session:
        del request.session['logged_in_user_name']

    return redirect('/login/') # ログインページへリダイレクト


'''
    Function Name: initial_entry_view
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/03
    Description:
        初回ログイン時のエントリーポイントビュー関数.
        ユーザーが初回ログインした際に、当日のログイン履歴があるかを確認し、
        ある場合はホームページへリダイレクトし、ない場合はログインフォームへリダイレクトする。
    Parameters: request: HTTPリクエストオブジェクト
    Returns: render or redirect: ホームページまたはログインフォームへリダイレクト
    Usage: initial_entry_view(request)
'''
def initial_entry_view(request):
    user_id = request.session.get('logged_in_user_id')
    if not user_id:
        return redirect('login_form')  # 未ログインなのでログインフォームへ

    # 当日のログイン履歴があるか確認
    today = localdate()
    try:
        user = UserCredentials.objects.get(user_id=user_id)
        has_today_log = LoginAttemptHistory.objects.filter(
            user=user,
            success=True,
            attempt_timestamp__date=today
        ).exists()

        if has_today_log:
            return render(request, 'home.html', {'user_name': request.session.get('logged_in_user_name')})
        else:
            return redirect('login_form')

    except UserCredentials.DoesNotExist:
        return redirect('login_form')


def login_form(request):
    return render(request, 'login_form.html')