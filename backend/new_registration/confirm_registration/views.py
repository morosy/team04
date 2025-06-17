# backend/confirm_registration/views.py (変更後)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# register_name アプリケーションの新しいヘルパー関数をインポート
from new_registration.register_name.views import _register_user_credentials 

@csrf_exempt
def confirm_registration_main(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_name = data.get('user_name')
            password = data.get('password')
            user_ID_int = data.get('user_ID')

            # 入力チェック (変更なし)
            if not all([user_name, password, user_ID_int is not None]):
                return JsonResponse({
                    'registration_success': False,
                    'errorMessage': 'Missing required fields (user_name, password, user_ID).'
                }, status=400)
            if not isinstance(user_ID_int, int):
                return JsonResponse({
                    'registration_success': False,
                    'errorMessage': 'User ID must be an integer.'
                }, status=400)

            registration_result = _register_user_credentials(user_name, password, user_ID_int)

            if registration_result.get('success'):
                return JsonResponse({
                    'registration_success': True,
                    'errorMessage': ''
                }, status=200)
            else:
                return JsonResponse({
                    'registration_success': False,
                    'errorMessage': f'Failed to register credentials: {registration_result.get("errorMessage", "Unknown error")}'
                }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({
                'registration_success': False,
                'errorMessage': 'Invalid JSON format.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'registration_success': False,
                'errorMessage': f'An unexpected error occurred: {str(e)}'
            }, status=500)
    else:
        # POST以外のリクエストは許可しない
        return JsonResponse({
            'registration_success': False,
            'errorMessage': 'Only POST requests are allowed.'
        }, status=405)