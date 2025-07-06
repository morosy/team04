from django.shortcuts import render

# Create your views here.
# backend/keiba_auth/login_ui/views.py

def login_form(request):
    """
    ログインフォームを表示するビュー。
    """
    return render(request, 'login_form.html')