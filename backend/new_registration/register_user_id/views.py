# backend/register_user_id/views.py (変更後)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserID
from django.db import IntegrityError

# ヘルパー関数: UserIDをデータベースに保存するロジック
# この関数は HttpRequest オブジェクトではなく、直接 user_id_int データを受け取る。
def _save_user_id_to_db(user_id_int):
    # 入力チェック
    if user_id_int is None:
        return {'success': False, 'errorMessage': 'User ID is missing.'}
    if not isinstance(user_id_int, int):
        return {'success': False, 'errorMessage': 'User ID must be an integer.'}
    if len(str(user_id_int)) != 8:
        return {'success': False, 'errorMessage': 'User ID must be 8 digits.'}

    # ユーザーIDをデータベースに保存
    try:
        user_entry = UserID(user_id=user_id_int)
        user_entry.save()
        return {'success': True, 'errorMessage': ''}
    except IntegrityError: # unique=True に違反した場合 (重複)
        return {'success': False, 'errorMessage': 'User ID already exists.'}
    except Exception as e:
        # その他の予期せぬエラー
        return {'success': False, 'errorMessage': f'An unexpected error occurred during ID saving: {str(e)}'}


@csrf_exempt # APIテスト中はこれを付けておくことが多い。本番環境では適切なCSRF対策が必要
def register_user_id(request):
    # このビュー関数は外部からのHTTPリクエストを受け取るためのもの
    if request.method == 'POST':
        try:
            # リクエストボディからJSONデータを取得
            data = json.loads(request.body)
            user_id_from_request = data.get('user_id')

            # 新しいヘルパー関数を呼び出す
            result = _save_user_id_to_db(user_id_from_request)

            if result['success']:
                return JsonResponse({'success': True, 'errorMessage': ''}, status=200)
            else:
                # ヘルパー関数からのエラーメッセージを返す
                status_code = 400 
                if "already exists" in result['errorMessage']:
                    status_code = 409 
                elif "unexpected error" in result['errorMessage']:
                    status_code = 500 
                return JsonResponse({'success': False, 'errorMessage': result['errorMessage']}, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'errorMessage': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            # その他の予期せぬエラー
            return JsonResponse({'success': False, 'errorMessage': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        # POST以外のリクエストは許可しない
        return JsonResponse({'success': False, 'errorMessage': 'Only POST requests are allowed.'}, status=405)