from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re 

# register_name _register_user_credentialsをインポート
from new_registration.register_name.views import _register_user_credentials # <-- ここを修正

@csrf_exempt
def name_registration_main(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_name = data.get('user_name')
            password = data.get('password')
            user_id_int = data.get('user_ID')

            # user_name のバリデーション (半角英数字、1文字以上10文字以内)
            if not user_name or not (1 <= len(user_name) <= 10) or not re.fullmatch(r'^[a-zA-Z0-9]+$', user_name):
                return JsonResponse({
                    'success': False,
                    'errorMessage': 'Invalid username format. Must be alphanumeric, 1-10 characters.'
                }, status=400)

            # password のバリデーション (半角英数字、8文字以上16文字以内)
            if not password or not (8 <= len(password) <= 16) or not re.fullmatch(r'^[a-zA-Z0-9]+$', password):
                return JsonResponse({
                    'success': False,
                    'errorMessage': 'Invalid password format. Must be alphanumeric, 8-16 characters.'
                }, status=400)

            # user_ID のバリデーション (int型、8桁)
            if user_id_int is None:
                return JsonResponse({
                    'success': False,
                    'errorMessage': 'User ID is missing.'
                }, status=400)
            if not isinstance(user_id_int, int):
                return JsonResponse({
                    'success': False,
                    'errorMessage': 'User ID must be an integer.'
                }, status=400)
            if not (10**7 <= user_id_int <= 10**8 - 1): # 8桁の範囲チェック
                return JsonResponse({
                    'success': False,
                    'errorMessage': 'User ID must be an 8-digit integer.'
                }, status=400)
            # --- バリデーション終了 ---

            # C2情報管理部（register_nameアプリ）のヘルパー関数を直接呼び出す
            # HTTPリクエストではなく、Pythonの関数として直接データを渡す
            registration_result = _register_user_credentials(user_name, password, user_id_int)

            if registration_result.get('success'):
                # 成功した場合、UIへの遷移はUI側でハンドリング
                return JsonResponse({
                    'success': True,
                    'errorMessage': ''
                }, status=200)
            else:
                # register_name からの登録失敗通知
                return JsonResponse({
                    'success': False,
                    'errorMessage': f'登録に失敗しました: {registration_result.get("errorMessage", "不明なエラー")}'
                }, status=200) # エラーメッセージの表示 (status=200は設計による)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'errorMessage': 'Invalid JSON format.'
            }, status=400)
        except Exception as e:
            # 予期せぬエラー
            return JsonResponse({
                'success': False,
                'errorMessage': f'予期せぬエラーが発生しました: {str(e)}'
            }, status=500)
    else:
        # POST以外のリクエストは許可しない
        return JsonResponse({
            'success': False,
            'errorMessage': 'Only POST requests are allowed.'
        }, status=405)

def registration_form_view(request):
    return render(request, 'registration_form.html')