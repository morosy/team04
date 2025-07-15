"""
    Designer: Mikami Kengo
    Description: ログイン機能のUIを表示するアプリ
    Note: このファイルは, ログイン機能を表示するためのものである。
"""
from django.shortcuts import render
def login_form(request):
    """
    ログインフォームを表示するビュー。
    """
    return render(request, 'login_form.html')