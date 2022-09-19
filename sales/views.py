import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, serializers, permissions

from account.point_models import WatchHistoryModel
from sales.models import VideoModel
from sales.serializers import GetPointSerializer, VideoListSerializer


class GetPoint(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
           Description
         """
    queryset = VideoModel.objects.all()
    serializer_class = GetPointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print('ok', str(serializer.validated_data.get('video_id')))
            WatchHistoryModel.save_history(request.user, serializer.validated_data.get('video_id'))

            # print('loyalty_amount', str(video.))

            return JsonResponse(status=requests.codes.ok, data={"success": True})
        return JsonResponse(status=requests.codes.bad, data={"success": False})
        # return TapaResponse(serializer.errors, status=False, message=gsms.VALIDATION_ERROR, status_code=400)


class VideoList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
           Description
         """
    permission_classes = [permissions.AllowAny]
    queryset = VideoModel.objects.all()
    serializer_class = VideoListSerializer
