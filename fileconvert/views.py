from django.shortcuts import render

import logging
import boto3


# ログの名前空間取得
logger = logging.getLogger('general')
# Textract Error
textractError = "server error"

#
# Convert画面表示
#
def index(request):

    # ボタンが押下されたら実行
    if "convert_progress" in request.POST:
        # ログ出力
        logger.info("Convertを開始します")

        # ファイルをフォームから入手
        fileObj = request.FILES['cutomfile[]']

        # Textract送受信開始
        resultTextract = textract_transceiver(fileObj.temporary_file_path())

        # エラーが返却された場合は戻る
        if resultTextract == textractError:
            return render(request, 'convert.html')

        # ログ出力
        logger.info(resultTextract)

    # ログ出力
    logger.info("Convert画面を表示します")
    
    return render(request, 'convert.html')

#
# Textract送受信用関数
#
def textract_transceiver(uploadFiles):
    # Amazon Textract client
    textractClient = boto3.client('textract', region_name="ap-southeast-1")

    try:
        # 画像ファイルを開く
        # With文が終わるとファイルを閉じてメモリを解放する
        with open(uploadFiles, 'rb') as file:
            data = file.read()
        # data = Image.open(uploadFiles)

        # Amazon Textractを呼び出し、レスポンスをキャッチ
        response = textractClient.detect_document_text(
            Document={
                'Bytes': data
            }
        )

        # レスポンスから文字列のみを抜き取る
        responseStr = "Response Start"
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                responseStr += '\n' + item["Text"]

    except Exception as e:
        logger.exception("Textractとの通信に失敗しました")

        # エラーを返却
        responseStr = textractError

    return responseStr