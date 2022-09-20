from django.urls import path
from .views import *

urlpatterns = [
    path('course/', ListCreateCourseAPIView.as_view(), name='get_post_course'),
    path('course/<int:pk>/', RetrieveUpdateDestroyCourseAPIView.as_view(), name='get_delete_update_course'),
]