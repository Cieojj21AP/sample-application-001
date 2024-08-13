from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from accounts.models import CustomUser as User
from accounts.forms import AccountsUpdateForm

import logging


# ログの名前空間取得
logger = logging.getLogger('general')

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

#
# アカウント詳細確認・変更画面
#
def account_detail(request):

    # ログインしていない場合、ログイン画面に遷移する
    if not request.user.id:
        return redirect('/account/login')
        
    # ボタンが押下されたら実行
    if "accounts_confirm" in request.POST:
        # ログ出力
        logger.info("アカウント情報を変更します")

        try:
            _instance = get_object_or_404(User, pk=request.user.id)
            form = AccountsUpdateForm(request.POST, instance=_instance)
            if form.is_valid():
                post = form.save(commit=False)
                # DBにコミット
                post.save()

        except Exception as e:
            # ログ出力
            logger.exception("アカウント情報変更に失敗しました")

    # ログ出力
    logger.info("アカウント情報変更画面を表示します")
    # ユーザー情報取得
    userObject = get_object_or_404(User, pk=request.user.id)

    # 初期値設定
    initialContext={
        'username':userObject.username,
        'email':userObject.email,
        'last_name':userObject.last_name,
        'first_name':userObject.first_name,
        'zipcode':userObject.zipcode,
        'address1':userObject.address1,
        'address2':userObject.address2,
    }

    # フォームに入力する
    form = AccountsUpdateForm(initialContext)
    
    # アカウント詳細確認・変更画面に遷移
    return render(request, 'accountsDetail.html', {'accountsForm': form})

#
# What画面表示
#
def what(request):
    return render(request, 'what.html')
