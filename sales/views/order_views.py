import os
from datetime import datetime

from rest_framework import permissions, exceptions, status, serializers
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListCreateAPIView, ListAPIView

from sales.models import *

from sales.serializers.order_serializers import OrderSerializer, CreateOrderSerializer
from sales.utils import time_calculator
from uo_core.custom_response_utils import CustomResponse


class OrderView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.none()

    def get(self, request, pk):
        # Note the use of `get_queryset()` instead of `self.queryset`
        item = Order.objects.filter(id=pk, buyer=request.user).first()
        if item:
            serializer = OrderSerializer(item)
            return Response(serializer.data)
        raise serializers.ValidationError(
            "Not Found"
        )

    @time_calculator
    def time(self):
        return 0

    def post(self, request, pk, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = request.user
            _cart = get_object_or_404(Cart, pk=pk)
            if _cart.user != request.user:
                raise exceptions.NotAcceptable("Not your Cart.")

            if _cart.check_product_quantity():
                raise exceptions.NotAcceptable("quantity of this product is out.")

            order_number = self.generate_order_number(_cart.user.id, _cart.id)

            order = Order().create_order(user, order_number,
                                         serializer.validated_data.get('phone'),
                                         serializer.validated_data.get('delivery'),
                                         serializer.validated_data.get('address'),
                                         serializer.validated_data.get('firstname'),
                                         serializer.validated_data.get('lastname'))
            for item in _cart.cart_items.all():
                _total = item.quantity * item.price
                order_items = OrderItem().create_order_item(order, item.product, item.quantity, _total)
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

        print('ser error', serializer.errors)
        return CustomResponse(status_code=status.HTTP_201_CREATED,
                              message='Validation error')

    def generate_order_number(self, key1, key2):
        order_number = (
                ("R0" if os.environ.get("DEBUG") == "TRUE" else "R")
                + ("1"+str(key1))[-5:]
                + ("2"+str(key2))[-5:]
                + str(datetime.timestamp(datetime.now()))[5:8])

        return order_number


class OrderViewList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(buyer=user).order_by('status').order_by('created_at')
        return queryset
