import logging

from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import status


log = logging.getLogger(__name__)


def _send_email(
    subject="",
    html_content="",
    recipients=[],
    files=None,
    from_email=settings.EMAIL_HOST_USER,
):
    try:
        if subject == "" or html_content == "" or recipients == '':
            log.error("No data provided to _send_email method.")
            return False
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipients,
            reply_to=[from_email],
        )
        email.content_subtype = "html"
        if files is not None:
            email.attach_file(files)
        _status = email.send()
        if _status:
            log.info(f"email to {recipients} send")
            return True, {}
    except Exception as e:
        log.error(e)
        responseData = {
            "message": str(e),
            "status": False,
            "status_code": status.HTTP_300_MULTIPLE_CHOICES,
        }
        return False, responseData
