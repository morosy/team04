"""
    Designer: Mikami Kengo
    Description: 新規登録機能のデータベースに仮入力を挿入するアプリ
    Note: このファイルは, ユーザが入力するまで仮のデータをデータベースに登録するものである。
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.db import connection 
import logging

@csrf_exempt
def generate_user_id_main(request):
    if request.method == 'POST':
        try:

            temp_username = f"t_{uuid.uuid4().hex[:8]}"
            temp_password = f"t_pass_{uuid.uuid4().hex[:8]}"

            generated_user_id = None
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (user_name, password, current_coin, login_count) VALUES (%s, %s, %s, %s)",
                    [temp_username, temp_password, 0, 0]
                )
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