from core_module import models
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context, Template, loader
from django.conf import settings


class DalyneMailSend(object):
    """class for DalyneMailSend"""
    def __init__(self, code, recipient_list: list):
        super(BrandSecureMailSend, self).__init__()
        self.code = code
        self.from_email = settings.EMAIL_FROM_C
        self.recipient_list = recipient_list

    def mailsend(self, mail_data: dict, attach=''):
        mail_content = models.MailTemplate.objects.get(code=self.code)
        subject = mail_content.subject
        template_variable = mail_content.template_variable.split(",")
        html_content = Template(mail_content.html_content)
        match_data_dict = {}
        for data in template_variable:
            if data.strip() in mail_data:
                match_data_dict[data.strip()] = mail_data[data.strip()]
        if match_data_dict:
            context_data = Context(match_data_dict)
            html_content = html_content.render(context_data)
            msg = EmailMessage(
                subject, html_content, self.from_email, self.recipient_list)
            msg.content_subtype = "html"
            msg.send()
        print("mail send Done..... ")
        return True


class EmailMixin(object):
    name = None
    subject_template_name = None
    html_body_template_name = None
    text_template = None
    cc = []

    def create_email(self, **ctx):
        try:
            subject = loader.render_to_string(self.subject_template_name, ctx)
            subject = ''.join(subject.splitlines())
        except:
            subject = ctx.get('subject_template_name')

        try:
            html_body = loader.render_to_string(self.html_body_template_name, ctx)
        except:
            html_body = ctx.get('html_body_template_name')
        text_body = loader.render_to_string(self.text_template, ctx)
        cc = ctx['cc'] if ctx.get('cc') else []

        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL,  [ctx['user_email']],
                                     cc=cc)
        msg.attach_alternative(html_body, 'text/html')
        msg.send()