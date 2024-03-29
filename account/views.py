import requests
from django.contrib.auth import logout
from rest_framework import viewsets, mixins, permissions, status, generics
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from account.message import (USER_FIND_ERROR,
                             ACCOUNT_WRONG_REPEAT_PASSWORD,
                             ACCOUNT_EMAIL_VERIFICATION_CODE_ERROR,
                             ACCOUNT_VALID_PASSWORD_ERROR)
from uo_core.global_message import GlobalMessage as gsms, GlobalMessage
from rest_framework.serializers import Serializer
from django.utils.translation import gettext_lazy as _
from account.serializers import *

from account.verify import confirm_code_phone
from uo_core.custom_response_utils import CustomResponse

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
JWT_EXPIRED_TIME = api_settings.JWT_EXPIRATION_DELTA


def confirm_code_email(email):
    return True


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        logout(request)
        return CustomResponse({}, True)


class CustomAuthToken(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return CustomResponse(message="Амжилттай", status_code=status.HTTP_200_OK, status=True,
                                  result=serializer.validated_data)
        return CustomResponse(message="Мэдээлэлээ шалгана уу.", result=serializer.errors, status=False,
                              status_code=status.HTTP_208_ALREADY_REPORTED)


class RegisterPhoneView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserPhoneSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, **kwargs):

        serializer = self.get_serializer(data=request.data)
        role = RoleModel.objects.get(code='user')
        dial_code = request.data.get("dial_code")

        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone")
            password = serializer.validated_data.get("password")

            if UserModel.objects.filter(phone=phone, role=role):
                return CustomResponse(message="Бүртгэлтэй хэрэглэгч байна.", status=False,
                                      status_code=status.HTTP_208_ALREADY_REPORTED)

            if confirm_code_phone(phone, dial_code):
                user = serializer.save(username=uuid.uuid4().hex)
                user.role = role
                user.phone = phone
                user.set_password(password)
                user.save()

                # payload = JWT_PAYLOAD_HANDLER(user)
                # jwt_token = JWT_ENCODE_HANDLER(payload)
                jwt_token = "asdasd"
                update_last_login(None, user)

                return CustomResponse(status=True, status_code=status.HTTP_200_OK,
                                      result={'token': jwt_token, 'user': UserProfileSerializer(instance=user).data})

            return CustomResponse(message="Баталгаажуулаагүй хэрэглэгч байна.", status=False,
                                  status_code=status.HTTP_208_ALREADY_REPORTED)


class RegisterEmailView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserEmailSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, **kwargs):

        serializer = self.get_serializer(data=request.data)
        role = RoleModel.objects.get(code='user')
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            if UserModel.objects.filter(email=email, role=role):
                return CustomResponse(message="Бүртгэлтэй хэрэглэгч байна.", status=False,
                                      status_code=status.HTTP_208_ALREADY_REPORTED)

            if confirm_code_email(email):
                user = serializer.save(username=uuid.uuid4().hex)
                user.role = role
                user.email = email
                user.set_password(password)
                user.save()

                refresh = MyTokenObtainPairSerializer.get_token(user)

                return CustomResponse(status=True, status_code=status.HTTP_200_OK,
                                      result={'token': str(refresh.access_token), 'user': UserProfileSerializer(instance=user).data})

            return CustomResponse(message="Баталгаажуулаагүй хэрэглэгч байна.", status=False,
                                  status_code=status.HTTP_208_ALREADY_REPORTED)


class GlobalVerificationEmailCode(generics.GenericAPIView):
    serializer_class = VerifyCodeEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse(status=True, status_code=status.HTTP_200_OK, result=serializer.validated_data)
        return CustomResponse(serializer.errors, status=False, status_code=status.HTTP_208_ALREADY_REPORTED)


class VerifyEmailCode(generics.GenericAPIView):
    serializer_class = VerifyCodeEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse(status=True, status_code=status.HTTP_200_OK, result=serializer.validated_data)
        return CustomResponse(serializer.errors, status=True, status_code=status.HTTP_208_ALREADY_REPORTED)


class CustomerRegisterView(generics.GenericAPIView):
    serializer_class = VerifyCodePhoneSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            phone = serializer.validated_data.get("phone")
            dial_code = serializer.validated_data.get("dial_code")
            role = RoleModel.objects.get(code='customer')
            user, created = UserModel.objects.update_or_create(phone=phone, dial_code=dial_code)
            if created:
                user.role = role
                user.phone = phone
                user.username = uuid.uuid4().hex
                user.save()

            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

            return CustomResponse(status=True, status_code=status.HTTP_200_OK,
                                  result={'token': jwt_token, "user": UserProfileSerializer(instance=user).data,
                                          "role": user.role.code})

        return CustomResponse(message="Баталгаажуулаагүй хэрэглэгч байна.", status=False,
                              status_code=status.HTTP_208_ALREADY_REPORTED)


# Хандалт хийсэн төхөөрөмжинийн мэдээлэл дээрээс JWT үүсгэж буцаах
# Төхөөрөмжийн мэдээлэлийг бааз-д хадгалах
class GuestJWT(generics.CreateAPIView):
    serializer_class = Serializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            # pass
            request.data['device_ip'] = x_forwarded_for.split(',')[0]
        else:
            request.data['device_ip'] = request.META.get('REMOTE_ADDR')

        request.data['device_name'] = request.META.get('SERVER_NAME')
        request.data['device_os'] = request.user_agent.os.family
        request.data['mac_add'] = request.user_agent.os.family
        serializer = DeviceSaveSerializer(data=request.data)

        if serializer.is_valid():
            return CustomResponse(serializer.validated_data)
        print('error ', serializer.errors)
        return CustomResponse(result=serializer.errors,
                              status=False,
                              message=_(gsms.TOKEN_VALIDATOR_ERROR),
                              status_code=requests.codes.already_reported, )


class ForgotPasswordView(generics.GenericAPIView):
    """
           [INFORMATION]

           200 - pass changed
           403 - REPEAT_PASSWORD error
           404 - USER_FIND_ERROR (no user with the email)
           406 - ACCOUNT_EMAIL_VERIFICATION_CODE_ERROR  (incorrect verify code)
           418 - Invalid  password

           other - error

       """

    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)

        if serializer.is_valid(raise_exception=True):
            user = None
            verify_code = serializer.validated_data.get("verify_code")
            email = serializer.validated_data.get("email")
            new_password = serializer.validated_data.get("new_password")
            reapet_password = serializer.validated_data.get("reapet_password")

            if new_password is reapet_password:
                return CustomResponse(message=ACCOUNT_WRONG_REPEAT_PASSWORD, status=False,
                                      status_code=status.HTTP_403_FORBIDDEN)

            try:
                user = UserModel.objects.get(email=email)
            except:
                return CustomResponse(message=USER_FIND_ERROR, status=False,
                                      status_code=status.HTTP_404_NOT_FOUND)

            if user.verify_code != verify_code:
                return CustomResponse(message=ACCOUNT_EMAIL_VERIFICATION_CODE_ERROR, status=False,
                                      status_code=status.HTTP_406_NOT_ACCEPTABLE)

            if check_password(user.password, new_password):
                return CustomResponse(message=ACCOUNT_VALID_PASSWORD_ERROR, status=False,
                                      status_code=status.HTTP_418_IM_A_TEAPOT)

            user.set_password(new_password)
            user.save()

            return CustomResponse(status=True, status_code=status.HTTP_200_OK, message="Амжилттай солигдлоо.")


class ForgotView(generics.GenericAPIView):
    """
        [INFORMATION]

        200 - sent code
        208 - already sent

        other - error

    """
    serializer_class = AuthEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)

        if serializer.is_valid(raise_exception=True):
            user = None
            email = serializer.validated_data.get("email")
            if email:
                if confirm_code_email(email):
                    try:
                        user = UserModel.objects.get(email=email)
                        _response = serializer.custom_validate(serializer.validated_data, user)
                        return CustomResponse(
                            status=_response.get("status"),
                            result=_response.get("data"),
                            message=_response.get("message", GlobalMessage.SUCCESS),
                            status_code=200 if _response.get("status", False) else 208
                        )

                    except Exception as e:
                        return CustomResponse(message=USER_FIND_ERROR, status=False,
                                              status_code=status.HTTP_404_NOT_FOUND)
                else:
                    return CustomResponse(message="Хэрэглэгч баталгаажуулаагүй байна", status=False,
                                          status_code=status.HTTP_404_NOT_FOUND)

            if user is None:
                return CustomResponse(message="Хэрэглэгч олдсонгүй", status=False,
                                      status_code=status.HTTP_208_ALREADY_REPORTED)

            return CustomResponse(status=True, status_code=status.HTTP_200_OK, message="Амжилттай солигдлоо.")


class UserProfileView(generics.ListCreateAPIView):
    """
        Хэрэглэгч мэдээлэл засах болон харах  API

    """
    serializer_class = UserUpdateSerializer
    queryset = UserModel.objects.none()

    # permission_classes = [IsUser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)
        return CustomResponse(result={"user": serializer.data}, status=True)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(instance=user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data,
                                  status_code=status.HTTP_200_OK,
                                  status=True)

        print('invalid', serializer.errors)
        return CustomResponse(serializer.errors,
                              status=False,
                              status_code=status.HTTP_208_ALREADY_REPORTED,
                              message=_(gsms.SAVE_ERROR))


class UpdateUserProfileView(generics.ListCreateAPIView):
    serializer_class = UserUpdateSerializer

    # permission_classes = [IsUser]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            print('valid', serializer.data)
            # if serializer.validated_data.get("first_name"):
            #     user.first_name = serializer.validated_data.get("first_name")
            # if serializer.validated_data.get("last_name"):
            #     user.last_name = serializer.validated_data.get("last_name")
            # # user.birthday = serializer.validated_data.get("birthday")
            # # user.gender = serializer.validated_data.get("gender")
            # # user.bank_account_number = serializer.validated_data.get("bank_account_number")
            # # user.bank_account_name = serializer.validated_data.get("bank_account_name")
            # # user.bank = serializer.validated_data.get("bank")
            # # user.home_address = serializer.validated_data.get("home_address")
            # # user.id_front = serializer.validated_data.get("id_front")
            # # user.id_rear = serializer.validated_data.get("id_rear")
            # # user.signature = serializer.validated_data.get("signature")
            # # user.selfie = serializer.validated_data.get("selfie")
            # user.save()
            return CustomResponse(serializer.data,
                                  status_code=status.HTTP_200_OK,
                                  status=True,
                                  message=_(gsms.SUCCESS))

        return CustomResponse(None,
                              status=False,
                              status_code=status.HTTP_208_ALREADY_REPORTED,
                              message=_(gsms.SAVE_ERROR))

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return CustomResponse(result={"user": serializer.data}, status=True)
