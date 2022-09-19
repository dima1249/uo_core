import _thread

from django.http import JsonResponse
from django.template.loader import get_template
from django.utils import timezone
from django.utils.crypto import get_random_string
from requests import Response
from rest_framework import serializers, status

from account.mail import Mail
from account.models import VerificationCodeModel


def confirm_code_email(email):
    try:
        confirm = VerificationCodeModel.objects.get(email=email)

    except Exception as e:
        return False

    if confirm.is_confirm:
        confirm.is_verify = False
        confirm.save()
        return True

    return False


def confirm_code_phone(phone, dial_code):
    try:
        confirm = VerificationCodeModel.objects.get(phone=phone, dial_code=dial_code)

    except Exception as e:
        return False
    if confirm.is_confirm:
        confirm.is_verify = False
        confirm.save()
        return True
    return False


def verification_code_email_send(to_mail='', browser_name='', operating_system=''):
    code = get_random_string(length=4, allowed_chars='1234567890')

    if to_mail is None:
        return False
    try:

        re_verify, created = VerificationCodeModel.objects.update_or_create(email=to_mail)

        print('re_verify', created, re_verify)
        re_verify.code = code
        re_verify.send_sms_time = timezone.now()
        re_verify.is_verify = False
        re_verify.save()

    except Exception as e:

        print('Exception', e)
        return False


    data = {'to': to_mail,
            'login_code': code,
            'browser_name': browser_name,
            'operating_system': operating_system}

    print('verification_code_email_send', data)

    response = login_password_sender(data)

    print('login_password_sender response ', response.status_code)

    if response.status_code == 200:
        return True
    return False


def verify_code_phone(phone, dial_code, code):
    try:
        verify = VerificationCodeModel.objects.get(dial_code=dial_code, phone=phone)
        if verify.try_count >= 10:
            return {'status': False, 'message': 'Таны өдөрийн хязгаарт хүрсэн байна.'}

        if verify.code == code:
            if verify.is_verify:
                return {'status': False, 'message': 'Код баталгаажсан байна.'}

            if not verify.is_active:
                return {'status': False, 'message': 'Кодын хугацаа дууссан байна.'}

            verify.is_verify = True
            verify.save()
            return {'status': True}

        else:
            verify.try_count += 1
            verify.save()
            return {'status': False}

    except Exception as e:
        return {'status': False, 'message': 'Код баталгаажуулхад алдаа гарлаа.'}


def verify_code_email(email, code):
    try:
        verify = VerificationCodeModel.objects.get(email=email, code=code)

    except Exception as e:
        return False

    if verify.is_active:
        verify.is_verify = True
        verify.save()
        return True

    return False


class MailSenderSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    to = serializers.EmailField()
    login_code = serializers.CharField()
    browser_name = serializers.CharField()
    operating_system = serializers.CharField()


def login_password_sender(data):
    serializer = MailSenderSerializer(data=data)
    if serializer.is_valid():
        mail = serializer.data.get("to")
        login_code = serializer.data.get("login_code")
        browser_name = serializer.data.get("browser_name")
        operating_system = serializer.data.get("operating_system")

        ctx = {
            'name': mail,
            'login_code': login_code,
            'browser_name': browser_name,
            'operating_system': operating_system,
        }
        body = get_template('login_password.html').render(ctx)
        try:
            _thread.start_new_thread(
                Mail.sender, (mail, 'Login password', body,))
            print(mail)
            return JsonResponse({"Success": "Mail sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Mail sent unsuccessfully!"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_208_ALREADY_REPORTED)
