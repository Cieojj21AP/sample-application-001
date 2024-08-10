from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ホーム画面
    path('home/', views.index, name='home'),
    # ホーム画面にリダイレクト
    path('', views.index_redirect, name='home_redirect'),

]