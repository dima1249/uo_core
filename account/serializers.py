import uuid

from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from uo_core.utills import get_country_info
from .models import *
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from account import message as msms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from dateutil.relativedelta import relativedelta

from .verify import verify_code_email, verify_code_phone, confirm_code_phone, verification_code_email_send

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
JWT_EXPIRED_TIME = api_settings.JWT_EXPIRATION_DELTA


class UserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    first_name = serializers.CharField(max_length=100, min_length=2, required=True)
    last_name = serializers.CharField(max_length=100, min_length=2, required=True)
    password = serializers.CharField(max_length=6, min_length=4, required=True)
    birthday = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=GENDER)


class UserUpdateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    first_name = serializers.CharField(max_length=100, min_length=2, required=False)
    last_name = serializers.CharField(max_length=100, min_length=2, required=False)
    password = serializers.CharField(max_length=6, min_length=4, required=False)
    birthday = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=GENDER, required=False)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id',
                  'first_name',
                  'last_name',
                  'birthday',
                  'gender',
                  'phone',
                  'dial_code',
                  'email',
                  'username'
                  )
        read_only_fields = ['dial_code', 'phone', 'email']


class UserMiniSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source="profile_picture")
    gender = serializers.CharField(source="gender")
    phone = serializers.CharField(source="phone")

    class Meta:
        model = UserModel
        fields = ["username", "profile_picture", "gender", "phone"]

class UserPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, min_length=8, required=True)
    dial_code = serializers.IntegerField(required=True)
    user_set = UserSerializer

    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'password', 'birthday', 'gender', 'phone', 'dial_code')


class UserEmailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=8, required=True)
    user_set = UserSerializer

    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'password', 'birthday', 'gender', 'email')


class VerificationCodePhoneSerializer(serializers.Serializer):
    dial_code = serializers.CharField(max_length=3, min_length=2, required=True)
    phone = serializers.CharField(max_length=16, min_length=8, required=True)

    def save(self):
        data = self.data
        phone = data.get('phone')
        dial_code = data.get('dial_code')

        # send = verification_code_phone_send(phone, dial_code)
        send = 2

        if send == 2:
            raise serializers.ValidationError("???????????????????????????? ?????? ???????????????? ??????????. ?????????? ?????????? ???????????????? ????!!!")

        if send == 3:
            raise serializers.ValidationError("???????? ?????????????? ???????????????? ???????????? ??????????.")

        if not send:
            raise serializers.ValidationError(
                "???????????????????????????? ?????? ???????????????? ?????????? ????????????. ???????????????? ?????????????? ?????????? ???????????? ?????")


class VerifyCodePhoneSerializer(serializers.Serializer):
    dial_code = serializers.IntegerField(required=True)
    phone = serializers.CharField(max_length=16, min_length=8, required=True)
    code = serializers.CharField(required=True)

    def save(self):
        data = self.data
        phone = data.get('phone')
        code = data.get('code')
        dial_code = data.get('dial_code')
        # verify = verify_code_phone(phone, dial_code, code)
        verify = {'status'}
        if verify['status'] == False:
            raise serializers.ValidationError(verify[
                                                  'message'] if 'message' in verify else "?????? ?????????????????????????????? ?????????? ????????????. ???????????????????? ?????????????? ?????????? ???????????? ?????")


class ForgotPasswordSerializer(serializers.Serializer):
    dial_code = serializers.IntegerField(required=False)
    new_password = serializers.CharField(required=True)
    reapet_password = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=16, min_length=8, required=False)

    def validate(self, data):
        phone = data.get("phone")
        email = data.get("email")
        dial_code = data.get("dial_code")

        if not phone and not email:
            raise serializers.ValidationError("???????? ?????????? ?????????? ???????????? ?????????????? ?????")

        if phone and email:
            raise serializers.ValidationError("???????? ?????????? ?????????? ???????????? ???????????? ?????????????? ?????")

        if phone:
            if not dial_code:
                raise serializers.ValidationError("dial_code ???????????????? ?????????????? ?????")

        return data


class VerificationCodeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def save(self):
        data = self.data
        request = self.context
        email = data.get('email')

        send = verification_code_email_send(email, request.user_agent.browser.family, request.user_agent.os.family)
        if not send:
            raise serializers.ValidationError(
                "?????? ?????????????????????????????? ?????????? ????????????. ???????????????????? ?????????????? ?????????? ???????????? ?????")


class VerifyCodeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, min_length=4, required=True)

    def save(self):
        data = self.data
        email = data.get('email')
        code = data.get('code')
        verify = verify_code_email(email, code)
        if not verify:
            raise serializers.ValidationError("?????? ?????????????????????????????? ?????????? ????????????. ???????????????????? ?????????????? ?????????? ???????????? ??????")


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, min_length=3, required=True)
    code = serializers.CharField(max_length=6, min_length=4, required=False)
    phone = serializers.CharField(max_length=255, min_length=8, required=False)
    dial_code = serializers.CharField(max_length=3, min_length=2, required=False)
    password = serializers.CharField(max_length=68, min_length=4, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = None
        password = data.get('password')
        phone = data.get('phone')
        email = data.get('email')
        dial_code = data.get('dial_code')

        if not phone and not email:
            raise serializers.ValidationError("???????? ?????????? ?????????? ???????????? ?????????????? ?????")

        if email:
            email = data.get('email')
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                # role = RoleModel.objects.get(code='user')
                # user = UserModel()
                # user.role = role
                # user.phone = phone
                # user.password = make_password(password)
                # user.username = uuid.uuid4().hex
                # user.save()
                raise serializers.ValidationError("???????????? ??-?????????????? ?????????????????? ?????????????? ??????????.")

        if phone:
            dial_code = data.get('dial_code')

            if not dial_code:
                raise serializers.ValidationError("???????????? ?????????? ?????????????? ?????")

            try:
                user = UserModel.objects.get(dial_code=dial_code, phone=phone)
            except UserModel.DoesNotExist:
                self.confirm_phone_code()
                role = RoleModel.objects.get(code='user')
                user = UserModel()
                user.role = role
                user.phone = phone
                user.dial_code = dial_code
                user.password = make_password(password)
                user.username = uuid.uuid4().hex
                user.save()

        if not check_password(password, user.password):
            raise serializers.ValidationError("???????????????????????? ?????????????? ??????, ???????? ???? ?????????? ??????????.")

        if not user.is_active:
            raise serializers.ValidationError("?????????????? ?????????????????? ??????????????????.")

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(msms.USER_FIND_ERROR)
        return {
            'user': UserProfileSerializer(instance=user).data,
            'role': user.role.code,
            'token': jwt_token,
        }

    def verify_phone_code(self):
        data = self.initial_data
        phone = data.get('phone')
        dial_code = data.get('dial_code')
        code = data.get('code')

        if not code:
            raise serializers.ValidationError("???????????????????????????? ?????????? ?????????????? ????!!!")

        verify = verify_code_phone(phone, dial_code, code)
        if verify['status'] == False:
            raise serializers.ValidationError(verify[
                                                  'message'] if 'message' in verify else "?????? ?????????????????????????????? ?????????? ????????????. ???????????????????? ?????????????? ?????????? ???????????? ?????")

    def confirm_phone_code(self):
        data = self.initial_data
        phone = data.get('phone')
        dial_code = data.get('dial_code')

        confirm = confirm_code_phone(phone, dial_code)
        if not confirm:
            raise serializers.ValidationError("?????????????????? ???????????????? ?????????? ????????????!!!")


class DeviceSaveSerializer(serializers.ModelSerializer):
    device_ip = serializers.CharField(max_length=16)
    device_name = serializers.CharField(max_length=255)
    device_os = serializers.CharField(max_length=255)

    class Meta:
        model = DeviceModel
        fields = ['device_ip', 'device_name',
                  'device_os', 'device_based_token']

    def validate(self, data):
        device = {'ip': data.get('device_ip'), 'name': data.get('device_name'), 'os': data.get('device_os')}
        device_token = JWT_ENCODE_HANDLER(device)

        user = UserModel.objects.get(username='guest_user')

        jwt_token = ""
        username = user.username
        password = 'd1c4fe4fe4b262fdf938d709'

        if DeviceModel.objects.filter(Q(device_based_token=device_token)).first() is None:
            DeviceModel.objects.create(device_ip=device['ip'], device_name=device['name'], device_os=device['os'],
                                       device_based_token=device_token, user=user)

        try:
            api_settings.JWT_EXPIRATION_DELTA = relativedelta(years=+1)
            user = authenticate(username=username, password=password)
            payload = JWT_PAYLOAD_HANDLER(user)
            payload['device_ip'] = device['ip']
            payload['device_name'] = device['name']
            payload['device_os'] = device['os']
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except Exception as e:
            print('JWT generation failed, ', str(e))
            # raise serializers.ValidationError(
            #     '?????????? ???????????????? ?????????? ???????????? '
            # )

        data = get_country_info(None, payload['device_ip'])
        version = dict()
        # android_os = AppVersion.objects.filter(device_os="android", is_active=True).first()
        # ios_os = AppVersion.objects.filter(device_os="ios", is_active=True).first()
        # huawei_os = AppVersion.objects.filter(device_os="huawei", is_active=True).first()
        # if android_os:
        #     version['android'] = android_os.version
        # if ios_os:
        #     version['ios'] = ios_os.version
        # if huawei_os:
        #     version['huawei'] = huawei_os.version
        api_settings.JWT_EXPIRATION_DELTA = relativedelta(days=+7)
        return {
            'JWToken': jwt_token,
            'role': user.role.code,
            'language': data.get('geoplugin_countryCode').upper(),
            'currency': data.get('geoplugin_countryCode').lower(),
            'version': version,
        }


class NotificationTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, allow_null=True)
    name = serializers.CharField(read_only=True)


class NotificationRecordSerializer(serializers.Serializer):
    email = serializers.ListField(child=NotificationTypeSerializer(), min_length=1)
    app = serializers.ListField(child=NotificationTypeSerializer(), min_length=1)
    phone = serializers.ListField(child=NotificationTypeSerializer(), min_length=1)


class StaticContentSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    reapet_password = serializers.CharField()
