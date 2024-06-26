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
    status_name = serializers.CharField(source='get_status_display')
    to_pay = serializers.SerializerMethodField()

    def get_to_pay(self, obj):
        return obj.to_pay()

    class Meta:
        model = Order
        fields = ["id",
                  "order_number",
                  "created_at",
                  "order_items",
                  "is_paid",
                  "to_pay",
                  "phone",
                  "address",
                  "firstname",
                  "lastname",
                  "delivery",
                  "status_name",
                  "status"]
        # exclude = "modified"


class CreateOrderSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255, min_length=8, required=True)
    delivery = serializers.BooleanField(required=True)
    address = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

    firstname = serializers.CharField(max_length=40, required=False)
    lastname = serializers.CharField(max_length=40, required=False)


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
