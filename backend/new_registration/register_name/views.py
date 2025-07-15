"""
    Designer: Mikami Kengo
    Description: 仮入力をユーザ入力に更新するアプリ
    Note: このファイルは, ユーザ入力をデータベースに登録するものである。
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserCredentials
from django.db import IntegrityError, transaction

from django.db import transaction, IntegrityError, connection

def _update_user_credentials(user_id_int, username, password):
    if not all([username, password, user_id_int is not None]):
        return {'success': False, 'errorMessage': 'Missing required fields (user_name, password, user_ID).'}

    try:
        with transaction.atomic():

            try:
                UserCredentials.objects.get(user_id=user_id_int)
            except UserCredentials.DoesNotExist:
                return {'success': False, 'errorMessage': f'User ID {user_id_int} does not exist.'}

            with connection.cursor() as cursor:

                cursor.execute(
                    "UPDATE users SET user_name = %s, password = %s WHERE user_ID = %s",
                    [username, password, user_id_int] 
                )

            try:
                with connection.cursor() as cursor:
                    user_name_for_sp = username[:10] 
                    print(f"DEBUG: Calling create_user_result_table with uid={user_id_int}, uname='{user_name_for_sp}'")
                    cursor.execute("CALL create_user_result_table(%s, %s)", [user_id_int, user_name_for_sp])
                print(f"DEBUG: user_result_table for user_ID {user_id_int} created successfully.")
            except Exception as e:
                print(f"ERROR: Failed to call create_user_result_table for user_ID {user_id_int}: {str(e)}")

            try:
                with connection.cursor() as cursor:
                    print(f"DEBUG: Calling create_friend_table with uid={user_id_int}")
                    cursor.execute("CALL create_friend_table(%s)", [user_id_int])
                print(f"DEBUG: friend_user_table for user_ID {user_id_int} created successfully.")
            except Exception as e:
                print(f"ERROR: Failed to call create_friend_table for user_ID {user_id_int}: {str(e)}")


            return {'success': True, 'errorMessage': ''}
    except IntegrityError:
        return {'success': False, 'errorMessage': 'Username already exists for another user.'}
    except Exception as e:
        # その他の予期せぬエラーはここに来る
        return {'success': False, 'errorMessage': f'An unexpected error occurred during user update: {str(e)}'}


@csrf_exempt
def register_name_main(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('user_name')
            password = data.get('password')
            user_id_int = data.get('user_ID')

            result = _update_user_credentials(user_id_int, username, password)

            if result['success']:
                return JsonResponse({'success': True, 'errorMessage': ''}, status=200)
            else:
                status_code = 400
                if "does not exist" in result['errorMessage']:
                    status_code = 404
                elif "already exists" in result['errorMessage']:
                    status_code = 409
                return JsonResponse({'success': False, 'errorMessage': result['errorMessage']}, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'errorMessage': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'errorMessage': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'errorMessage': 'Only POST requests are allowed.'}, status=405)