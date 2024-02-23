# from google.auth.transport import requests
# from google.oauth2 import id_token
# from account.message import *


class Google:

    @staticmethod
    def validate(token_id):
        return None
        # try:
        #     idinfo = id_token.verify_oauth2_token(
        #         token_id, requests.Request())
        #
        #     if 'accounts.google.com' in idinfo['iss']:
        #         return idinfo
        #
        # except:
        #     return TOKEN_EXPIRED_ERROR
