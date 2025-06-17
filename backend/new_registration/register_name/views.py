# backend/register_name/views.py (変更後)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserCredentials
from new_registration.register_user_id.models import UserID
from django.db import IntegrityError

def _register_user_credentials(username, password, user_id_int):
    # 入力チェック (ビュー関数から移動)
    if not all([username, password, user_id_int is not None]):
        return {'success': False, 'errorMessage': 'Missing required fields (user_name, password, user_id).'}
    if not isinstance(user_id_int, int):
        return {'success': False, 'errorMessage': 'User ID must be an integer.'}

    # ユーザーIDが存在するか確認 (ビュー関数から移動)
    try:
        user_id_instance = UserID.objects.get(user_id=user_id_int)
    except UserID.DoesNotExist:
        return {'success': False, 'errorMessage': f'User ID {user_id_int} does not exist in UserID table.'}

    # UserCredentialsを保存
    try:
        user_credentials = UserCredentials(
            user_id=user_id_instance, # UserIDインスタンスをセット
            username=username,
            password=password
        )
        user_credentials.save()
        return {'success': True, 'errorMessage': ''}
    except IntegrityError: # unique=True に違反した場合 (重複)
        return {'success': False, 'errorMessage': 'Username already exists or User ID is already linked.'}


@csrf_exempt
def register_name_main(request):
    # このビュー関数は外部からのHTTPリクエストを受け取るためのもの
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('user_name')
            password = data.get('password')
            user_id_int = data.get('user_id')

            # 新しいヘルパー関数を呼び出す
            result = _register_user_credentials(username, password, user_id_int)

            if result['success']:
                return JsonResponse({'success': True, 'errorMessage': ''}, status=200)
            else:
                # ヘルパー関数からのエラーメッセージを返す
                status_code = 400 # デフォルトはBad Request
                if "exist" in result['errorMessage'] or "linked" in result['errorMessage']:
                    status_code = 409 # Conflict
                elif "does not exist" in result['errorMessage']:
                    status_code = 404 # Not Found
                return JsonResponse({'success': False, 'errorMessage': result['errorMessage']}, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'errorMessage': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'errorMessage': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'errorMessage': 'Only POST requests are allowed.'}, status=405)