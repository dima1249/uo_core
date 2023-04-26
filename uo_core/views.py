from rest_framework import generics, permissions
from django.http import JsonResponse


class Health(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return JsonResponse({"message": "core system success"},
                            status=200
                            )
