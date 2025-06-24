# backend/new_registration/register_name/views.py (再掲)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserCredentials
from django.db import IntegrityError, transaction

def _update_user_credentials(user_id_int, username, password):
    if not all([username, password, user_id_int is not None]):
        return {'success': False, 'errorMessage': 'Missing required fields (user_name, password, user_ID).'}
    '''
    if not isinstance(user_id_int, int):
        return {'success': False, 'errorMessage': 'User ID must be an integer.'}
    '''

    try:
        with transaction.atomic():
            user_entry = UserCredentials.objects.get(user_id=user_id_int) # user_ID で取得

            user_entry.user_name = username
            user_entry.password = password # ★パスワードは必ずハッシュ化してください！
            user_entry.save()
            return {'success': True, 'errorMessage': ''}
    except UserCredentials.DoesNotExist:
        return {'success': False, 'errorMessage': f'User ID {user_id_int} does not exist.'}
    except IntegrityError:
        return {'success': False, 'errorMessage': 'Username already exists for another user.'}
    except Exception as e:
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