from rest_framework import serializers
from sales.models import SellItemModel, CartItem
from sales.serializers import SellItemTypeSerializer


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellItemModel
        fields = (
            "title",
            "desc",
            "category",
            "price",
            "brand",
        )


class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
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
    type_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["product",
                  "quantity",
                  "price",
                  "in_store",
                  "size",
                  "color",
                  "type",
                  "type_id",
                  ]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem

        fields = ["product",
                  "quantity",
                  "size",
                  "color",
                  "type",
                  ]
        extra_kwargs = {'quantity': {'required': True}}
