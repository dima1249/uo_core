import uuid

from account.models import UserModel, RoleModel
from rest_framework_jwt.settings import api_settings

from account.serializers import UserProfileSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
JWT_EXPIRED_TIME = api_settings.JWT_EXPIRATION_DELTA


def register_social_user_apple(first_name, last_name, sub, email):
    if not UserModel.objects.filter(email=email).exists():
        user = UserModel()

    else:
        user = UserModel.objects.get(email=email)

    if first_name is None:
        user.first_name = email.split('@')[0]
    else:
        user.first_name = first_name

    if last_name is None:
        user.last_name = email.split('@')[0]
    else:
        user.last_name = last_name

    user.apple_user_id = sub
    user.role = RoleModel.objects.get(code='user')
    user.username = uuid.uuid4().hex
    user.email = email
    user.is_staff = False
    user.save()

    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)

    return {
        'user': UserProfileSerializer(instance=user).data,
        'token': jwt_token,
    }


def register_social_user(provider, user_id, email, name, picture=None):
    if not UserModel.objects.filter(email=email).exists():
        user = UserModel()

    else:
        user = UserModel.objects.get(email=email)

    if provider == 'facebook':
        user.fb_user_id = user_id
    if provider == 'google':
        user.google_user_id = user_id

    user.role = RoleModel.objects.get(code='user')
    user.first_name = name.split(' ')[0]
    user.last_name = name.split(' ')[1]
    user.username = uuid.uuid4().hex
    user.email = email
    user.profile_picture = picture
    user.is_staff = False
    user.save()

    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)

    return {
        'user': UserProfileSerializer(instance=user).data,
        'token': jwt_token,
    }
