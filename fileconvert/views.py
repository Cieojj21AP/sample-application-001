from django.shortcuts import render

import logging
import boto3


# ログの名前空間取得
logger = logging.getLogger('general')
# Textract Error
textractError = "server error"
# Translate Error
translateError = "server error"

#
# Convert画面表示
#
def index(request):

    # ボタンが押下されたら実行
    if "convert_progress" in request.POST:
        # ログ出力
        logger.info("Convertを開始します")

        # ファイルをフォームから入手
        # temporaryFiles = request.FILES['cutomfile[]']
        temporaryFiles = request.FILES.getlist('cutomfile[]')

        # Textract送受信開始
        # resultTextract = textract_transceiver(temporaryFiles.temporary_file_path())
        resultTextract = textract_transceiver(temporaryFiles)

        # エラーが返却された場合は戻る
        if resultTextract == textractError:
            return render(request, 'convert.html')
        
        # Translate送受信開始
        resultTranslate = translate_transceiver(resultTextract)

        # エラーが返却された場合は戻る
        if resultTranslate == translateError:
            return render(request, 'convert.html')
        
        # ログ出力
        # logger.info(resultTextract)
        
        # ログ出力
        logger.info(resultTranslate)

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
        # ページ番号
        pageNum = 1
        responseStr = "page" + str(pageNum)
        for uploadFile in uploadFiles:
            # 画像ファイルを開く
            # With文が終わるとファイルを閉じてメモリを解放する
            with open(uploadFile.temporary_file_path(), 'rb') as file:
                data = file.read()

            # Amazon Textractを呼び出し、レスポンスをキャッチ
            response = textractClient.detect_document_text(
                Document={
                    'Bytes': data
                }
            )

            # レスポンスから文字列のみを抜き取る
            if not pageNum == 1:
                responseStr += '\n' + '\n' + "page" + str(pageNum)
            for item in response["Blocks"]:
                if item["BlockType"] == "LINE":
                    responseStr += '\n' + item["Text"]

            # ページ番号に1を足す
            pageNum += 1

    except Exception as e:
        # ログ出力
        logger.exception("Textractとの通信に失敗しました")

        # エラーを返却
        responseStr = textractError

    return responseStr


#
# Translate送受信用関数
#
def translate_transceiver(srcText):
    # Amazon Translate client
    translateClient = boto3.client('translate', region_name="ap-southeast-1")
    srcLang = 'auto'
    trgLang = 'ja'

    try:
        # Amazon Translateを呼び出し、レスポンスをキャッチ
        response = translateClient.detect_document_text(
            Text=srcText,
            SourceLanguageCode = srcLang,
            TargetLanguageCode = trgLang,
        )

    except Exception as e:
        # ログ出力
        logger.exception("Translateとの通信に失敗しました")

        # エラーを返却
        responseStr = translateError

    return responseStr