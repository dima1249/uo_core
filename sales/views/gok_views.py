import os
from datetime import datetime

from rest_framework import permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListCreateAPIView, CreateAPIView

from sales.banks.qpay import QpayV2
from sales.models import *

from sales.serializers.order_serializers import OrderSerializer, CreateOrderSerializer
from sales.utils import time_calculator

qpay = QpayV2()


class CreateInvoiceView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderSerializer

    # serializer_class = OrderSerializer

    @time_calculator
    def time(self):
        return 0

    def post(self, request, *args, **kwargs):
        _result = qpay.create_invoice(
            "tesat123", 100
        )
        if "name" in _result and _result["name"] == "ERROR":
            print('error')
        return Response("error", status=status.HTTP_201_CREATED)
