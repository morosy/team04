from django.shortcuts import render
from .logic.ranking import ranking_main_process
from .logic.friend import (
    friend_request_process,
    friend_request_accept_process,
    friend_request_decline_process,
)

'''
def home(request):
    return render(request, 'core/home.html')
'''

'''
    data: 2025/06/23
    カレントディレクトリをfrontendに変更
'''
def home(request):
    return render(request, 'home.html')



def ranking_view(request):
    if request.method == 'POST':
        result = ranking_main_process(request.POST)
        return render(request, 'core/ranking.html', {'user_list': result})
    return render(request, 'core/ranking.html')

def friend_request_view(request):
    if request.method == 'POST':
        msg = friend_request_process(request.POST.get("user_id"))
        return render(request, 'core/friend-request.html', {'message': msg})
    return render(request, 'core/friend-request.html')

def friend_accept_view(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist("check_box")
        msg = friend_request_accept_process(user_ids)
        return render(request, 'core/friend-acceptance.html', {'message': msg})
    return render(request, 'core/friend-acceptance.html')

def friend_decline_view(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist("check_box")
        msg = friend_request_decline_process(user_ids)
        return render(request, 'core/friend-acceptance.html', {'message': msg})
    return render(request, 'core/friend-acceptance.html')
