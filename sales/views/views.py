from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from django_filters import rest_framework as filters
from django.utils.translation import ugettext_lazy as _
from sales.models import *
from sales.serializers import ProductCategorySerializer, BrandModelSerializer, ProductSerializer


class ListCreateCategoryAPIView(ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategoryModel.objects.all()
    permission_classes = [permissions.AllowAny]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = CourseFilter

    def perform_create(self, serializer):
        pass
        # Assign the user who created the movie
        # serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyCategoryAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategoryModel.objects.all()
    permission_classes = [permissions.AllowAny]


class ListCreateBrandAPIView(ListCreateAPIView):
    serializer_class = BrandModelSerializer
    queryset = BrandModel.objects.all()
    permission_classes = [permissions.AllowAny]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = CourseFilter

    def perform_create(self, serializer):
        pass
        # Assign the user who created the movie
        # serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyBrandAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BrandModelSerializer
    queryset = BrandModel.objects.all()
    permission_classes = [permissions.AllowAny]


class ListCreateProductAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = SellItemModel.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        pass


class RetrieveUpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = SellItemModel.objects.all()
    permission_classes = [permissions.AllowAny]
