import re

from rest_framework import serializers
from sales.models import SellItemModel, CartItem, SellItemAttributes, Cart
from sales.serializers import SellItemTypeSerializer, ProductImageSerializer


class CartProductSerializer(serializers.ModelSerializer):
    pictures = ProductImageSerializer(many=True, source='image_product')

    class Meta:
        model = SellItemModel
        fields = (
            "title",
            "desc",
            "category",
            "price",
            "pictures",
            "brand",
        )


class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = ["id",
                  "product",
                  "quantity",
                  "size",
                  "color",
                  "type",
                  "price",
                  ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id",
                  "cart",
                  "product",
                  "quantity",
                  "size",
                  "color",
                  "type",
                  "price",
                  ]

class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)
    type = SellItemTypeSerializer()
    # type_name = serializers.IntegerField()
    type_id = serializers.IntegerField()
    buy_limit = serializers.SerializerMethodField()

    def get_buy_limit(self, obj):
        attr = SellItemAttributes.objects.filter(item=obj.product)
        if obj.type:
            attr = attr.filter(type=obj.type)
        if obj.color:
            attr = attr.filter(color=obj.color)
        if obj.size:
            if re.match('^\d+$',obj.size):
                attr = attr.filter(size=float(obj.size))
            else:
                attr = attr.filter(size_unit=obj.size)

        return abs(attr[0].quantity) if len(attr) else 1

    class Meta:
        model = CartItem
        fields = ["product",
                  "quantity",
                  "id",
                  "buy_limit",
                  "price",
                  "in_store",
                  "size",
                  "color",
                  "color_code",
                  "type",
                  "type_id",
                  ]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem

        fields = ["quantity",]
        extra_kwargs = {'quantity': {'required': True}}
