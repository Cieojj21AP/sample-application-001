from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
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

    # ボタンが押下されたら実行
    if "accounts_confirm" in request.POST:
        # ログ出力
        logger.info("アカウント情報変更を登録します")

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

        # ユーザIDをもとにDBに照会
        # user = get_object_or_404(User, pk=request.user.id)
        # context = {
        #     'user': user,
        # }

    # URL接続時
    # ログ出力
    logger.info("アカウント情報変更画面を表示します")
    # 初期値設定
    initialContext={
        'username':request.user.username,
        'email':request.user.email,
        'last_name':request.user.last_name,
        'first_name':request.user.first_name,
        'zipcode':request.user.zipcode,
        'address1':request.user.address1,
        'address2':request.user.address2,
    }
    form = AccountsUpdateForm(initialContext)
    
    # アカウント詳細確認・変更画面に遷移
    return render(request, 'accountsDetail.html', {'accountsForm': form})
