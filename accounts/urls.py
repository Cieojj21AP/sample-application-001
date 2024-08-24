from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ホーム画面
    path('home/', views.index, name='home'),
    # ホーム画面にリダイレクト
    path('', views.index_redirect, name='home_redirect'),
    # アカウント詳細確認・変更画面
    path('account/detail', views.account_detail, name='account_detail'),
    # what画面
    path('what', views.what, name='what'),

    # Stripe支払い画面
    path('billing/', views.billing_index, name='stripe_config'),
    # Stripe設定画面
    path('billing/config/', views.stripe_config, name='stripe_config'),
    # 支払い遷移画面
    path('billing/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    # 支払い成功画面
    path('billing/success/', views.success, name='success'),
    # 支払い失敗画面
    path('billing/cancel/', views.cancel, name='cancel'),
    # Webhookエンドポイント
    path('billing/webhook/api/v1/events', views.webhook_receiver, name='webhook_receiver'),
]