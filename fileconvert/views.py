from django.shortcuts import render

import logging


# ログの名前空間取得
logger = logging.getLogger('general')

#
# Convert画面表示
#
def index(request):
    # ログ出力
    logger.info("Convert画面を表示します")
    
    return render(request, 'convert.html')
