@ECHO OFF
REM ���[�J������Stripe��Webhook���N������
REM �G���h�|�C���g��ݒ肷��
SET endpoint=localhost:8080/billing/webhook/api/v1/events

stripe listen --forward-to %endpoint%