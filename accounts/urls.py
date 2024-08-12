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

]