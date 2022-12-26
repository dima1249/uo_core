import os
from datetime import datetime

from rest_framework import permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from sales.models import *

from sales.serializers.order_serializers import OrderSerializer
from sales.utils import time_calculator


class OrderView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(buyer=user).order_by('status').order_by('created_at')
        return queryset

    @time_calculator
    def time(self):
        return 0

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        _cart = get_object_or_404(Cart, pk=pk)
        if _cart.user != request.user:
            raise exceptions.NotAcceptable("Not your Cart.")

        if _cart.check_product_quantity():
            raise exceptions.NotAcceptable("quantity of this product is out.")

        order_number = self.generate_order_number(_cart.user.id, _cart.id)

        order = Order().create_order(user, order_number, "", True)
        for item in _cart.cart_items.all():
            _total = item.quantity * item.product.price
            order_item = OrderItem().create_order_item(order, item.product, item.quantity, _total)
        # serializer = OrderItemMiniSerializer(order)
        # push_notifications(
        #     user,
        #     "Request Order",
        #     "your order: #" + str(order_number) + " has been sent successfully.",
        # )
        _cart.delete_cart_item()
        self.time()
        print("order_created", order.id)
        serializer = OrderSerializer(order)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def generate_order_number(self, key1, key2):
        order_number = (
                ("R00" if os.environ.get("DEBUG") == "TRUE" else "R")
                + str(key1)
                + "-"
                + str(key2)
                + "-"
                + str(datetime.timestamp(datetime.now()))[5:8])

        return order_number
