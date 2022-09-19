import json
from time import time

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import google, facebook
from .register import register_social_user, register_social_user_apple
from account.message import *
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
JWT_EXPIRED_TIME = api_settings.JWT_EXPIRATION_DELTA

class FacebookSocialAuthSerializer(serializers.Serializer):

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            picture = user_data['picture']['data']['url']
            return register_social_user(user_id=user_id, email=email, name=name, provider='facebook', picture=picture)
        except Exception as identifier:
            raise serializers.ValidationError(TOKEN_EXPIRED_ERROR)


class GoogleSocialAuthSerializer(serializers.Serializer):
    token_id = serializers.CharField()

    def validate_token_id(self, token_id):
        user_data = google.Google.validate(token_id)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(TOKEN_EXPIRED_ERROR)

        # if user_data['aud'] != "618747949610-gjdqiu2qveu5s1h7mhjs3kh2stfd88h1.apps.googleusercontent.com":
        #     raise serializers.ValidationError(_(sms.WHO_ARE_YOU_ERROR))

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(email=email, name=name, user_id=user_id, provider=provider)


APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"
APPLE_PUBLIC_KEY = None
APPLE_KEY_CACHE_EXP = 60 * 60 * 24
APPLE_LAST_KEY_FETCH = 0
APPLE_APP_ID = "com.tapatrip"


def _fetch_apple_public_key():
    # Check to see if the public key is unset or is stale before returning
    global APPLE_LAST_KEY_FETCH
    global APPLE_PUBLIC_KEY

    if (APPLE_LAST_KEY_FETCH + APPLE_KEY_CACHE_EXP) < int(time()) or APPLE_PUBLIC_KEY is None:
        key_payload = requests.get(APPLE_PUBLIC_KEY_URL).json()
        APPLE_PUBLIC_KEY = RSAAlgorithm.from_jwk(json.dumps(key_payload["keys"][0]))
        APPLE_LAST_KEY_FETCH = int(time())
    return APPLE_PUBLIC_KEY


def _decode_apple_user_token(apple_user_token):
    public_key = _fetch_apple_public_key()

    try:
        token = jwt.decode(apple_user_token, public_key, audience=APPLE_APP_ID, algorithm="RS256", verify=False)
    # except jwt.exceptions.ExpiredSignatureError as e:
    #     raise Exception("That token has expired")
    # except jwt.exceptions.InvalidAudienceError as e:
    #     raise Exception("That token's audience did not match")
    except Exception as e:
        print(e)
        # raise Exception("An unexpected error occoured")

    return token


class AppleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True, allow_null=True)
    last_name = serializers.CharField(required=True, allow_null=True)

    def validate(self, value):
        token = self.initial_data.get("auth_token")
        first_name = self.initial_data.get("first_name")
        last_name = self.initial_data.get("last_name")
        try:
            decode = _decode_apple_user_token(token)

        except Exception as e:
            print(e)
            raise ValidationError("Have not access")

        print(decode)
        return register_social_user_apple(first_name=first_name, last_name=last_name, sub=decode.get("sub"), email=decode.get("email"))
