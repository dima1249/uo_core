from rest_framework import generics, permissions
from django.http import JsonResponse
from rest_framework import serializers


class Health(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return JsonResponse({"message": "core system success"},
                            status=200
                            )
