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


class SellItemTypeSerializer(serializers.ModelSerializer):
    # picture = serializers.ImageField(required=True)

    class Meta:
        model = SellItemTypeModel
        exclude = [
            "created_at",
            "updated_at",
            "deleted_at"
        ]


class SellItemAttributeSerializer(serializers.ModelSerializer):
    type = SellItemTypeSerializer()
    type_id = serializers.IntegerField()

    class Meta:
        model = SellItemAttributes
        exclude = ["item", ]


class SellItemAttributeTypeSerializer(serializers.ModelSerializer):
    type = SellItemTypeSerializer()

    class Meta:
        model = SellItemAttributes
        exclude = ["item", "id"]


class ProductSerializer(serializers.ModelSerializer):
    # travel_image = TravelImageSerializer(many=True)
    pictures = ProductImageSerializer(many=True, source='image_product')

    quantities = SellItemAttributeSerializer(many=True, source='attributes')
    types = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    total_quantity = serializers.IntegerField()
    colors = serializers.SerializerMethodField()

    # SellItemAttributes

    category_name = serializers.ReadOnlyField(source="category.name")
    brand_name = serializers.ReadOnlyField(source="brand.name")

    def get_types(self, obj):
        qs = obj.attributes.values('type').distinct().values_list('type', flat=True)
        return SellItemTypeSerializer(SellItemTypeModel.objects.filter(id__in=qs), many=True).data

    def get_sizes(self, obj):
        return obj.attributes.exclude(size__isnull=True).values('size', 'size_unit').distinct().all()

    def get_colors(self, obj):
        return obj.attributes.exclude(color__isnull=True).values('color', 'color_code').distinct().all()

    # def get_types(self, obj):
    #     qs = obj.attributes.values('type').distinct().values_list('type', flat=True)
    #     return SellItemTypeSerializer(SellItemTypeModel.objects.filter(id__in=qs), many=True).data
    #
    #

    class Meta:
        model = SellItemModel
        fields = "__all__"
        read_only_fields = [
            "title",
            "desc",
            "price",
            # "pictures",
            "category",
            "total_quantity",
            "category_name",
            "brand",
            "brand_name",
        ]
