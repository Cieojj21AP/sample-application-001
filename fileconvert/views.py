from django.shortcuts import render

import logging


# ログの名前空間取得
logger = logging.getLogger('general')

#
# Home画面表示
#
def index(request):
    return render(request, 'home.html')
