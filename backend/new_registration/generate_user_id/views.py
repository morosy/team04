# backend/generate_user_id/views.py (大幅修正)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid # 一時的なユニークな値を生成するために追加

# UserCredentials モデルを使って users テーブルに書き込む
from new_registration.register_name.models import UserCredentials

@csrf_exempt
def generate_user_id_main(request):
    if request.method == 'POST':
        try:
            # データベースの AUTO_INCREMENT に user_ID の生成を任せる
            # username と password は NOT NULL なので、一時的な値を設定
            # ★注意: 本番環境では、ここでパスワードをハッシュ化すること！
            temp_username = f"t_{uuid.uuid4().hex[:8]}" # これで 1+8 = 9文字
            temp_password = f"t_pass_{uuid.uuid4().hex[:8]}" # これで 7+8 = 15文字 (OK)

            # UserCredentials のインスタンスを作成し、user_ID は指定しない
            new_user_entry = UserCredentials(
                user_name=temp_username,
                password=temp_password,
                current_coin=0,
                login_count=0
                # login_timestamp は auto_now_add=True (もしあれば) または default=timezone.now で自動設定
            )
            new_user_entry.save() # これでデータベースが user_ID を自動生成し、保存される

            # 保存された new_user_entry から自動生成された user_ID を取得
            generated_user_id = new_user_entry.pk

            return JsonResponse({
                'user_ID': generated_user_id,
                'registration_success': True,
                'errorMessage': ''
            }, status=200)

        except Exception as e:
            # データベースエラー（例：一時ユーザー名の重複など、非常に稀）やその他の予期せぬエラー
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