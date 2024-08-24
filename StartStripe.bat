@ECHO OFF
REM ローカル環境のStripeのWebhookを起動する
REM エンドポイントを設定する
SET endpoint=localhost:8080/billing/webhook/api/v1/events

stripe listen --forward-to %endpoint%