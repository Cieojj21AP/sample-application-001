from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

#
# Home画面表示
#
def index(request):
    return render(request, 'home.html')

#
# Home画面にリダイレクトする
#
def index_redirect(request):
    response = redirect('/home/')
    return response