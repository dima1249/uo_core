import _thread
import email

from django.http import JsonResponse
from django.template.loader import get_template
from django.test import TestCase

# Create your tests here.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_address = 'zumomn@gmail.com'
sender_pass = 'KYTWM6TwfE4q9AYf'

class Mail(object):
    @staticmethod
    def sender(mail, subject, body, files=None, mail_counter=None, CC=[]):
        # The mail addresses and password
        SENDER = 'noreply@zumo.com'
        message = MIMEMultipart()
        message['From'] = SENDER
        message['To'] = mail
        message['Subject'] = subject

        message['Message-id'] = email.utils.make_msgid()
        message['Date'] = email.utils.formatdate()
        texthtml = MIMEText(body, _subtype='html', _charset='UTF-8')
        message.attach(texthtml)

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, mail, text)
        session.quit()
        print('Mail Sent')

        #
        # if mail_counter is None:
        #     tagtaa = TagtaaMail()
        #     tagtaa.email = msg['To']
        #     tagtaa.body = texthtml
        #     tagtaa.count = 0
        #     tagtaa.status = 0
        #     tagtaa.save()
        #
        # if files:
        #     with open(files, "rb") as fil:
        #         part = MIMEApplication(fil.read(), Name=basename(files))
        #         part['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
        #         msg.attach(part)
        # try:
        #     server = smtplib.SMTP(HOST, PORT)
        #     server.ehlo()
        #     server.starttls()
        #     server.ehlo()
        #     server.login(USERNAME_SMTP, PASSWORD_SMTP)
        #     server.sendmail(SENDER, mail, msg.as_string())
        #     server.close()
        # except Exception as e:
        #     print("Error: ", e)
        #     tagtaa_error = TagtaaMail.objects.filter(email=msg['To'], body=texthtml).first()
        #     tagtaa_error.count = tagtaa_error.count + 1
        #     tagtaa_error.status = 1
        #     tagtaa_error.description = 'count=' + str(tagtaa_error.count) + ', reason' + str(e)
        #     tagtaa_error.save()
        #     print(tagtaa_error.count)
        #     time.sleep(10)
        #     if tagtaa_error.count <= 3:
        #         Mail.sender(mail, subject, body, files, mail_counter=tagtaa_error.count)
        #     else:
        #         print('MAIL sending FAILED RETRY !')
        # else:
        #     print('Mail sent successfully!')
