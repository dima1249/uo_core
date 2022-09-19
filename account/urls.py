from django.urls import path, include
from rest_framework import routers

# from account.social_auth.views import GoogleSocialAuthView, FacebookSocialAuthView, AppleSocialAuthView
from account.social_auth.views import FacebookSocialAuthView, GoogleSocialAuthView
from account.views import *

account = routers.DefaultRouter()
account.register(r'register/phone', RegisterPhoneView)
account.register(r'register/email', RegisterEmailView)
#
urlpatterns = [
    path('', include(account.urls)),
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
    #     path('apple/', AppleSocialAuthView.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('logout/', Logout.as_view()),
    path('global_verification_code/email/', GlobalVerificationEmailCode.as_view()),
    path('verify_code/email/', VerifyEmailCode.as_view()),
    path('guest_jwt/', GuestJWT.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('profile/', UserProfileView.as_view()),

]
