from core.async_queue.celery_config import Celery_Dependency
import smtplib
from settings.setting import settings
from src.schemas import Email_Field
from email.message import EmailMessage
import ssl
from src.apps.auth.dependency import celery_app

app = celery_app.get_app()


@app.task(max_retries=3, name="send_verify_email")
def send_verify_email(user_email: Email_Field, token: str) -> None:
    
    url = f"{settings.frontend_url}/auth/confirm_user?token={token}"
    msg = EmailMessage()
    msg.set_content(url)
    msg["To"] = user_email
    msg["From"] = settings.email_settings.email_login
    msg["Subject"] = "Подтерждение аккаунтаа"

    with smtplib.SMTP_SSL(
            host=settings.email_settings.email_host,
            port=settings.email_settings.email_port,
            timeout=30.0,
            context=ssl.create_default_context()
        ) as smtp:
            smtp.login(user=settings.email_settings.email_login, password=settings.email_settings.email_password.get_secret_value())
            smtp.send_message(msg=msg)

