from django.shortcuts import render
import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
import random

def home(request):
    return render(request, 'home.html')

def select_ticket(request):
    return render(request, 'select_ticket.html')

def display_race1(request):
    return render(request, 'display_race1.html')

def display_race2(request):
    return render(request, 'display_race2.html')

#勝つ馬のレーンの番号を決める関数
def make_output_race():
    #簡略化するために1~5の数字を重複しないようにランダムで三つ返す
    return random.sample(range(1, 6), 3)

def get_user_coin(user_id):
    try:
        user = User.objects.get(id=user_id)
        coin = user.current_coin
    except User.DoesNotExist:
        coin = 0
        
    return coin

def update_user_coin(user_id, change_coin):
    try:
        user = User.objects.get(id=user_id)
        user.current_coin += change_coin  # 例: +50 や -10
        user.save()  # 変更をDBに保存
        return True
    except User.DoesNotExist:
        return False

def reserve_output_race(user_id, date, category, result, change_coin, current_coin):
    user = User.objects.get(id=user_id)
    if(result):
        user.number_of_wins += 1
    else:
        user.number_of_losses += 1
    user.save()

def submit_race1(request):
    if request.method == 'POST':
        horse = request.POST.get('horse')  # '1'〜'5'（文字列）
        coins = request.POST.get('coins')  # 例: '10'
        
        #print(f"選ばれたレーン: {horse}, 賭けたコイン: {coins}")
        ranks = make_output_race()

        if horse == ranks[0]:
            result = '的中'
            change_coin = 3-1 * coins
            update_user_coin(user_id, change_coin)
        else:
            resutl = 'ハズレ'
            change_coin = -coins
            update_user_coin(user_id, change_coin)

        return render(request, 'race_result.html', {
            'rank1': ranks[0],
            'rank2': ranks[1],
            'rank3': ranks[2],
            'coin': change_coin
            'result': 
        })

    return redirect('home')  # POST以外のアクセスは戻す

def display_race2(request):
    lanes = [1, 2, 3, 4, 5]
    return render(request, 'display_race2.html', {'lanes': lanes})


def submit_race2(request):
    if request.method == 'POST':
        rank1 = request.POST.get('rank1')
        rank2 = request.POST.get('rank2')
        rank3 = request.POST.get('rank3')
        coin = request.POST.get('coin')

        # 入力チェック（同じレーンがないか、数字かどうか）
        if rank1 == rank2 or rank1 == rank3 or rank2 == rank3:
            return render(request, 'display_race2.html', {
                'error': '同じレーンを重複して選んでいます。'
            })

        # 必要ならintに変換
        try:
            r1, r2, r3 = int(rank1), int(rank2), int(rank3)
            coin = int(coin)

        except ValueError:
            return render(request, 'display_race2.html', {
                'error': '数字を正しく入力してください。'
            })

        # 結果画面へ
        ranks = make_output_race()
        if r1 == ranks[0] and r2 == ranks[1] and r3 == ranks[2]:
            result = '的中'
        else:
            result = 'ハズレ'

        return render(request, 'race_result.html', {
            'rank1': ranks[0],
            'rank2': ranks[1],
            'rank3': ranks[2],
            'coin': coin
            'result': 
        })

    return redirect('home')

def get_user_coin(user_id):
    try:
        user = User.objects.get(id=user_id)
        coin = user.current_coin
    except User.DoesNotExist:
        coin = 0
        
    return coin

def update_user_coin(user_id, change_coin):
    try:
        user = User.objects.get(id=user_id)
        user.current_coin += change_coin  # 例: +50 や -10
        user.save()  # 変更をDBに保存
        return True
    except User.DoesNotExist:
        return False

def reserve_output_race(user_id, date, category, result, change_coin, current_coin):
    user = User.objects.get(id=user_id)
    if(result):
        user.number_of_wins += 1
    else:
        user.number_of_losses += 1
    user.save()


def main_race(user_id):
