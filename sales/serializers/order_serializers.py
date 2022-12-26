from rest_framework import serializers

from account.serializers import UserMiniSerializer
from sales.models import *
# UserMiniSerializer
from sales.serializers import ProductSerializer, CartProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()

    class Meta:
        model = OrderItem

        exclude = ["created_at",
                   "updated_at",
                   "deleted_at", ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ["id",
                  "order_number",
                  "order_items",
                  "is_paid",
                  "status"]
        # exclude = "modified"


class OrderMiniSerializer(serializers.ModelSerializer):
    # address = AddressSerializer(required=False)
    buyer = UserMiniSerializer(required=False)

    class Meta:
        model = Order
        exclude = "modified"


class OrderItemMiniSerializer(serializers.ModelSerializer):
    order = OrderMiniSerializer(required=False, read_only=True)
    product = ProductSerializer(required=False, read_only=True)

    class Meta:
        model = OrderItem
        exclude = "modified"
