from celery import shared_task, Task
from celery.utils.log import get_task_logger
from core_module.mailer import DalyneMailSend, EmailMixin
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


logger = get_task_logger(__name__)


# @shared_task
# def send_mail_forgot_password(name, email):
#     mail_id = email
#     mail_data = {
#         'name': name,
#         'email': urlsafe_base64_encode(force_bytes(email))
#         }
#     mail_class = DalyneMailSend('FPE', [mail_id])
#     mail_response = mail_class.mailsend(mail_data)
#     print('mail_response...', mail_response)
#     return True


@shared_task
def send_mail_for_account_activation(email, name, domain, uid, token, ip, password):
    mail_id = email
    mail_data = {
        'name': name,
        'domain': domain,
        'uid': uid,
        'token': token
        }
    mail_class = DalyneMailSend('UEV', [mail_id])
    mail_response = mail_class.mailsend(mail_data)
    print('mail_response...', mail_response)
    return True


class SendOTPNotificationOnEmail(Task, EmailMixin):
    """sending opt to the respective user's registered e-mail"""

    name = "Email Notifications"
    subject_template_name = None
    html_body_template_name = None
    text_template = None

    def run(self, **ctx):
        self.subject_template_name = ctx.get('subject_template_name', None)
        self.html_body_template_name = ctx.get('html_body_template_name', None)
        self.text_template = ctx.get('text_template', None)

        self.create_email(**ctx)
