from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from accounts.models import CustomUser as User
from accounts.forms import AccountsUpdateForm
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionCustomer as SubCus
from django.contrib.auth.decorators import login_required
import stripe

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


################################################################
# stripe用
################################################################
#
# Stripe支払い画面表示
#
def billing_index(request):
    # ログインしていない場合、ログイン画面に遷移する
    if not request.user.id:
        return redirect('/account/login')
    
    return render(request, 'billing/index.html')

#
# Stripe設定用の処理
#
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

#
# 支払い画面に遷移させるための処理
#
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        # ログ出力
        logger.info("サブスクリプションを実施します")

        # 現在のドメインつきURLを取得する
        domain_url = "{0}://{1}".format(request.scheme, request.get_host()) + '/billing/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # サブスクリプションの形式を識別する
        if "query" in request.GET:
            queryParam = request.GET.get("query")
            if queryParam == settings.SUBSCRIPTION_MONTHLY_LIMITED:
                stripPriceId = settings.STRIPE_PRICE_ID_MONTHLY_LIMITED
            elif queryParam == settings.SUBSCRIPTION_YEARLY_LIMITED:
                stripPriceId = settings.STRIPE_PRICE_ID_YEARLY_LIMITED
            else:
                # ログ出力
                logger.exception("サブスクリプションの形式が不正です")
                return redirect('/billing/')

        else:
            # ログ出力
            logger.exception("サブスクリプションの形式が指定されていません")
            return redirect('/billing/')

        try:
            # stripeのAPIにアクセスし、支払いを委託する
            checkout_session = stripe.checkout.Session.create(
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                client_reference_id=request.user.id,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        # 'price': settings.STRIPE_PRICE_ID,
                        'price': stripPriceId,
                        'quantity': 1,
                    }
                ]
            )

            # ログ出力
            logger.info("{id: " + checkout_session['id'] + ", client_reference_id: " + checkout_session['client_reference_id'] + "}")
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

#
# 支払いに成功した後の画面
#
def success(request):
    # 支払い成功以外の場合はリダイレクト
    if not request.GET.get('session_id'):
        return redirect('/home/')

    return render(request, 'billing/success.html')

#
# 支払いに失敗した後の画面
#
def cancel(request):
    return render(request, 'billing/cancel.html')


#
# Webhookからの情報を常に受ける
#
@csrf_exempt
def webhook_receiver(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    event_type = event['type']
    # Handle the checkout.session.completed event
    if event_type == 'checkout.session.completed':
        ### チェックアウト成功＝サブスクスタート時のアクションを書きましょう。
        session = event['data']['object']
        webhook_client_reference_id    = session.get('client_reference_id')  #リファレンスID(3.1.でStripeに飛ばしたclient_reference_id)
        webhook_stripe_customer_id     = session.get('customer')             #カスタマーID
        webhook_stripe_subscription_id = session.get('subscription')         #サブスクリプションID

        #自サービスのデータにStripe決済データを登録する等Updateしましょう。
        print('Payment succeeded!')
        print(webhook_client_reference_id)
        print(webhook_stripe_customer_id)
        print(webhook_stripe_subscription_id)

    elif event_type == 'customer.subscription.trial_will_end':
        #トライアル期間が終了する時のアクションを書きましょう
        print('Subscription trial will end')

    elif event_type == 'customer.subscription.created':
        # 省略
        print('Subscription created %s', event.id)

    elif event_type == 'customer.subscription.updated':
        # 省略
        print('Subscription created %s', event.id)

    elif event_type == 'customer.subscription.deleted':
        # 省略
        # handle subscription canceled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print('Subscription canceled: %s', event.id)

    return HttpResponse(status=200)