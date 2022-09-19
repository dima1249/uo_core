import facebook
from account.message import *

class Facebook:

    @staticmethod
    def validate(auth_token):
        
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email,first_name,last_name,picture')
            return profile
        except:
            return TOKEN_EXPIRED_ERROR
