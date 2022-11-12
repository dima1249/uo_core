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


class ProductImageSerializer(serializers.ModelSerializer):
    # picture = serializers.ImageField(required=True)

    class Meta:
        model = ProductImageModel
        # title
        # picture
        # order
        # fields = ['title', 'picture']
        exclude = ["product", "order", "id"]


class ProductSerializer(serializers.ModelSerializer):
    # travel_image = TravelImageSerializer(many=True)
    pictures = ProductImageSerializer(many=True, source='image_product')

    category_name = serializers.ReadOnlyField(source="category.name")
    brand_name = serializers.ReadOnlyField(source="brand.name")

    # insurance_name = serializers.ReadOnlyField(source="insurance.name")

    class Meta:
        model = SellItemModel
        fields = "__all__"
        read_only_fields = [
            "title",
            "desc",
            "price",
            # "pictures",
            "quantity",
            "category",
            "category_name",
            "brand",
            "brand_name",
        ]
