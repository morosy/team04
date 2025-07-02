# backend/new_registration/generate_user_id/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.db import connection # データベース接続のために追加
import logging

# UserCredentials モデルは、直接レコードを保存しないので、ここでインポートする必要はないが、
# 必要に応じて他の用途で使う場合は残しても良い。
# from new_registration.register_name.models import UserCredentials

@csrf_exempt
def generate_user_id_main(request):
    if request.method == 'POST':
        try:
            # データベースの AUTO_INCREMENT に user_ID の生成を任せる
            # username と password は NOT NULL なので、一時的な値を設定
            # ※注意: 実際のDBスキーマでこれらのフィールドがNOT NULLかつデフォルト値がない場合、
            #   一時的な有効な値を渡す必要があります。
            #   UUIDベースの一時名/パスワードは衝突の可能性が非常に低い安全な方法です。
            temp_username = f"t_{uuid.uuid4().hex[:8]}"
            temp_password = f"t_pass_{uuid.uuid4().hex[:8]}"

            generated_user_id = None
            with connection.cursor() as cursor:
                # 生のSQL INSERT文を使用してレコードを挿入し、自動生成されたIDを取得
                # users テーブルの user_ID が AUTO_INCREMENT になっていることを前提とする
                # current_coinとlogin_countはnull許容なので0を挿入
                cursor.execute(
                    "INSERT INTO users (user_name, password, current_coin, login_count) VALUES (%s, %s, %s, %s)",
                    [temp_username, temp_password, 0, 0]
                )
                # 挿入された行の最後のAUTO_INCREMENT IDを取得 (MySQLの場合)
                cursor.execute("SELECT LAST_INSERT_ID()")
                generated_user_id = cursor.fetchone()[0]

            if generated_user_id:
                return JsonResponse({
                    'user_ID': generated_user_id,
                    'registration_success': True,
                    'errorMessage': ''
                }, status=200)
            else:
                return JsonResponse({
                    'user_ID': None,
                    'registration_success': False,
                    'errorMessage': 'Failed to generate user ID from database.'
                }, status=500)

        except Exception as e:
            # データベースエラーなどの予期せぬエラー
            logging.error(f"An unexpected error occurred during ID generation: {str(e)}")
            return JsonResponse({
                'user_ID': None,
                'registration_success': False,
                'errorMessage': f'An unexpected error occurred during ID generation: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'user_ID': None,
            'registration_success': False,
            'errorMessage': 'Only POST requests are allowed.'
        }, status=405)