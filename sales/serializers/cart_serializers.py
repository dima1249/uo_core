from rest_framework import serializers
from sales.models import SellItemModel, CartItem


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellItemModel
        fields = (
            "title",
            # "seller",
            "quantity",
            "price",
            # "image",
        )


class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = ["id","cart", "product", "quantity"]


class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]
