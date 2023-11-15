from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from celery import shared_task
from app.main_users.models import CustomUser, UserInfo
from .models import EmailToken
from app.mails.utils import _send_email

from django.core.mail import EmailMessage


@shared_task
def new_user_register(user_id):
    token, _ = EmailToken.objects.get_or_create(user_id=user_id, purpose="confirm")
    subject = "Письмо кандидату о регистрации"
    from_email = settings.EMAIL_HOST_USER
    to_email = [token.user.email]
    context = {
        "user": token.user.email,
        "uid": urlsafe_base64_encode(force_bytes(user_id)),
        "token": token,
    }
    message = get_template("user/register.html").render(context)
    msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
    msg.content_subtype = "html"
    msg.send()


@shared_task
def password_reset_link_created(user_id):
    """отправляем письмо с для смены пароля"""
    token, _ = EmailToken.objects.get_or_create(
        user_id=user_id, purpose="reset_link"
    )
    subject = 'Восстановление доступа'
    from_email = settings.EMAIL_HOST_USER
    to_email = [token.user.email]
    context = {
        'username': token.user.username,
        'uid': urlsafe_base64_encode(force_bytes(user_id)),
        'token': token
    }
    message = get_template('mails/password_restore.html').render(context)
    msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    
    
    
    # message = render_to_string(
    #     "mails/Password_RESTORE.html",
    #     {
    #         "user": token,
    #         "domain": domain,
    #         "uid": urlsafe_base64_encode(force_bytes(user_id)),
    #         "token": token,
    #     },
    # )
    # return _send_email(
    #     subject="Ссылка для сброса пароля отправлена на ваш адрес электронной почты",
    #     html_content=message,
    #     recipients=[token.user.email],
    # )


@shared_task
def user_email_change(user_id, domain, new_email):
    """
    отправляем письмо с подтверждением смены почты
    """
    token, _ = EmailToken.objects.get_or_create(user_id=user_id, purpose="email")

    message = render_to_string(
        "user/email_change.html",
        {
            "user": token,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user_id)),
            "token": token,
            "new_email": new_email,
        },
    )

    msg = EmailMultiAlternatives(
        "Ссылка для смены электронной почты отправлена "
        "на ваш текущий адрес электронной почты",
        message,
        settings.EMAIL_HOST_USER,
        [token.user.email],
    )
    msg.send()


@shared_task
def send_become_founder(user_id, email_to):
    subject = "Письмо кандидату о становлений Основателем"
    user = UserInfo.objects.filter(user__id=user_id).first()
    context = {
            "first_name": user.first_name if user else None,
            "middle_name": user.last_name if user else None,
            "father_name": user.father_name if user else None
        }
    
    from_email = settings.EMAIL_HOST_USER
    message = render_to_string("mails/Founder.html", context=context)
    msg = EmailMessage(subject, message, to=[email_to], from_email=from_email)
    msg.content_subtype = "html"
    msg.send()
