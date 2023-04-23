import email
import os
import smtplib
from email.header import Header
from django.template.loader import get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from account.message import ACCOUNT_VERIFY_YOUR_EMAIL
from uo_core.settings import DEBUG


class Mail(object):

    @staticmethod
    def send_verification_email(email, context, language="en"):
        context["language"] = language
        code = context["code"]
        mail_title = Mail.get_email_header(
            mail_type=context["type"], code=context["code"]
        )
        mail_body = Mail.get_email_body(
            context=context
        )
        _to = email
        _CC = []
        if os.environ.get("DEBUG") == "TRUE":
            _CC.append("do.damdinsuren@gmail.com")
        else:
            _CC.append("usukh_od.dev@gmail.com")

        return Mail().sender(
            _to,
            str(mail_title),
            mail_body,
            None,
            _CC,
        )


    @staticmethod
    def sender(mail, subject, body, files=None, CC=[]):
        SENDER = "noreply@usukh-od.com"
        USERNAME_SMTP = os.environ.get("SMTP_USERNAME")
        PASSWORD_SMTP = os.environ.get("SMTP_PASSWORD")
        HOST = os.environ.get("SMTP_HOST")
        PORT = os.environ.get("SMTP_PORT")
        cc = [os.environ.get("CC_TRACK_MAIL")] + CC

        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(subject)
        msg["From"] = "%s <%s>" % (Header("USUKH-OD.COM"), SENDER)
        msg["To"] = mail

        # msg['To'] = ", ".join(mail)
        # msg["Bcc"] = ", ".join(cc)
        msg["Message-id"] = email.utils.make_msgid()
        msg["Date"] = email.utils.formatdate()

        texthtml = MIMEText(body, _subtype="html", _charset="UTF-8")
        msg.attach(texthtml)
        # if files:
        #     if DEBUG and os.environ.get("AWS_S3") != "TRUE":
        #         for file_name in files:
        #             with open(f"media/{file_name}", "rb") as fil:
        #                 part = MIMEApplication(fil.read(), Name=basename(file_name))
        #                 part[
        #                     "Content-Disposition"
        #                 ] = 'attachment; filename="%s"' % basename(file_name)
        #                 msg.attach(part)
        #     else:
        #         from tapatrip_backend.settings import MEDIA_URL
        #
        #         for file_name in files:
        #             response = requests.get(f"{MEDIA_URL}{file_name}")
        #             part = MIMEApplication(response.content, Name=basename(file_name))
        #             part[
        #                 "Content-Disposition"
        #             ] = 'attachment; filename="%s"' % basename(file_name)
        #             msg.attach(part)
        to_address = [mail]
        # to_address = [*set([mail] + cc)] if not DEBUG else [mail]

        try:
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            server.sendmail(SENDER, to_address, msg.as_string())
            server.close()
        except Exception as e:
            print("Mail sender exception:", e)
            return False
        else:
            print("Mail sent successfully!")
            return True





    @staticmethod
    def get_email_body(context):
        mail_template = None
        if context["type"] == "success":
            mail_template = get_template(f"email_v2/success.html")
        elif context["type"] == "canceled":
            mail_template = get_template(f"email_v2/canceled.html")
        elif context["type"] == "verification" or context["type"] == "register":
            mail_template = get_template("email_v2/verification.html")
        mail_body = mail_template.render(context) if mail_template else None
        return mail_body

    @staticmethod
    def get_email_header(mail_type, code=None):
        title = None
        if mail_type == "confirmed":
            pass
            # title = messages.FLIGHT_ORDER_CONFIRM_MAIL_TITLE
        elif mail_type == "verification":
            title = "[{}] {}".format(code, str(ACCOUNT_VERIFY_YOUR_EMAIL))
        return title

    @staticmethod
    def get_email_footer(mail_type):
        return True