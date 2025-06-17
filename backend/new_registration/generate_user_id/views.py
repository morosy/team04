# backend/generate_user_id/views.py (変更後)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json
# from register_user_id.models import UserID # UserIDの重複チェックは引き続き必要なので残す
from new_registration.register_user_id.models import UserID # <-- パスを修正

# register_user_id アプリケーションの新しいヘルパー関数をインポート
from new_registration.register_user_id.views import _save_user_id_to_db 

@csrf_exempt
def generate_user_id_main(request):
    if request.method == 'POST': # UIからの要求はPOSTを想定
        try:
            generated_user_id = None
            max_attempts = 10 # 重複しないIDを生成するための試行回数

            for _ in range(max_attempts):
                # 8桁のランダムな整数を生成
                new_id = random.randint(10000000, 99999999)
                # 重複チェック (register_user_idアプリのUserIDモデルを使用)
                if not UserID.objects.filter(user_id=new_id).exists():
                    generated_user_id = new_id
                    break

            if generated_user_id is None:
                # 規定回数試行しても重複しないIDが生成できなかった場合
                return JsonResponse({
                    'user_ID': None,
                    'registration_success': False,
                    'errorMessage': 'Failed to generate a unique user ID after multiple attempts.'
                }, status=500)


            registration_result = _save_user_id_to_db(generated_user_id)

            if registration_result.get('success'):
                return JsonResponse({
                    'user_ID': generated_user_id,
                    'registration_success': True,
                    'errorMessage': ''
                }, status=200)
            else:
                # 登録失敗の場合
                return JsonResponse({
                    'user_ID': generated_user_id,
                    'registration_success': False,
                    'errorMessage': f'Failed to register user ID: {registration_result.get("errorMessage", "Unknown error")}'
                }, status=200)

        except Exception as e:
            # その他の予期せぬエラー
            return JsonResponse({
                'user_ID': None,
                'registration_success': False,
                'errorMessage': f'An unexpected error occurred during ID generation: {str(e)}'
            }, status=500)
    else:
        # POST以外のリクエストは許可しない
        return JsonResponse({
            'user_ID': None,
            'registration_success': False,
            'errorMessage': 'Only POST requests are allowed.'
        }, status=405)