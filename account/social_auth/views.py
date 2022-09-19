from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from uo_core.custom_response_utils import CustomResponse
from .serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer, AppleSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['token_id'])
        return CustomResponse(data)


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])

        return CustomResponse(data)


class AppleSocialAuthView(GenericAPIView):
    serializer_class = AppleSocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)

        return CustomResponse(data)
