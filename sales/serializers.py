from django_filters import rest_framework as filters
from rest_framework import serializers
from sales.models import *


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = '__all__'



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellItemModel
        fields = '__all__'





