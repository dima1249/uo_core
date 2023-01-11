import requests
from django.contrib.auth import logout
from django.contrib.auth.models import update_last_login
from django.utils.crypto import get_random_string
from rest_framework import viewsets, mixins, permissions, status, generics
from rest_framework.views import APIView

from uo_core.global_message import GlobalMessage as gsms
from rest_framework.serializers import Serializer
from django.utils.translation import gettext_lazy as _

from account.models import *
from account.serializers import *

from account.verify import confirm_code_phone
from uo_core.custom_response_utils import CustomResponse


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
        if serializer.is_valid():
            return CustomResponse(message="Амжилттай", status_code=status.HTTP_200_OK, status=True,
                                  result=serializer.validated_data)
        return CustomResponse(serializer.errors, status=False, status_code=status.HTTP_208_ALREADY_REPORTED)


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

                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)

                return CustomResponse(status=True, status_code=status.HTTP_200_OK,
                                      result={'token': jwt_token, 'user': UserProfileSerializer(instance=user).data})

            return CustomResponse(message="Баталгаажуулаагүй хэрэглэгч байна.", status=False,
                                  status_code=status.HTTP_208_ALREADY_REPORTED)


class GlobalVerificationEmailCode(generics.GenericAPIView):
    serializer_class = VerificationCodeEmailSerializer
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
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)

        if serializer.is_valid(raise_exception=True):
            user = None
            phone = serializer.validated_data.get("phone")
            email = serializer.validated_data.get("email")
            dial_code = serializer.validated_data.get("dial_code")
            new_password = serializer.validated_data.get("new_password")
            reapet_password = serializer.validated_data.get("reapet_password")

            if new_password is reapet_password:
                return CustomResponse(message="Давтаж оруулсан нууц үг буруу байна.", status=False,
                                      status_code=status.HTTP_208_ALREADY_REPORTED)

            if phone:
                if confirm_code_phone(phone, dial_code):
                    try:
                        user = UserModel.objects.get(dial_code=dial_code, phone=phone)
                    except:
                        return CustomResponse(message="Хэрэглэгч олдсонгүй", status=False,
                                              status_code=status.HTTP_208_ALREADY_REPORTED)
                else:
                    return CustomResponse(message="Хэрэглэгч баталгаажуулаагүй байна", status=False,
                                          status_code=status.HTTP_208_ALREADY_REPORTED)

            if email:
                if confirm_code_email(email):
                    try:
                        user = UserModel.objects.get(email=email)
                    except:
                        return CustomResponse(message="Хэрэглэгч олдсонгүй", status=False,
                                              status_code=status.HTTP_208_ALREADY_REPORTED)
                else:
                    return CustomResponse(message="Хэрэглэгч баталгаажуулаагүй байна", status=False,
                                          status_code=status.HTTP_208_ALREADY_REPORTED)

            if user is None:
                return CustomResponse(message="Хэрэглэгч олдсонгүй", status=False,
                                      status_code=status.HTTP_208_ALREADY_REPORTED)

            if check_password(user.password, new_password):
                return CustomResponse(message="Өмнөх нууц үгээс өөр нууц үг оруулна уу?", status=False,
                                      status_code=status.HTTP_208_ALREADY_REPORTED)

            user.set_password(new_password)
            user.save()

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
        if serializer.is_valid():
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

        print('invalid', serializer.errors)
        return CustomResponse(serializer.errors,
                              status=False,
                              status_code=status.HTTP_208_ALREADY_REPORTED,
                              message=_(gsms.SAVE_ERROR))

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return CustomResponse(result={"user": serializer.data}, status=True)
