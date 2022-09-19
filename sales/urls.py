from django.urls import path, include
from rest_framework import routers

from sales.views import *

router = routers.DefaultRouter()

# Old Section
router.register(r'videos', VideoList, 'list_videos')
router.register(r'point', GetPoint, 'get_point')
router.register(r'user_data', GetPoint, 'get_point')
router.register(r'', GetPoint, 'get_point')
router.register(r'', GetPoint, 'get_point')
router.register(r'', GetPoint, 'get_point')

# router.register(r'videos', VideoList, 'list_videos')
# router.register(r'videos', VideoList, 'list_videos')

urlpatterns = [
    path('rest/', include(router.urls)),
    # path('test/', test_view),
]
