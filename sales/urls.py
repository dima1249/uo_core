from django.urls import path
from .views import *

urlpatterns = [
    path('brand/', ListCreateBrandAPIView.as_view(), name='get_post_brands'),
    path('brand/<int:pk>/', RetrieveUpdateDestroyBrandAPIView.as_view(), name='get_delete_update_brand'),

    path('product/', ListCreateProductAPIView.as_view(), name='get_post_products'),
    path('product/<int:pk>/', RetrieveUpdateDestroyProductAPIView.as_view(), name='get_delete_update_product'),

    path('category/', ListCreateCategoryAPIView.as_view(), name='get_post_categories'),
    path('category/<int:pk>/', RetrieveUpdateDestroyCategoryAPIView.as_view(), name='get_delete_update_category'),
]