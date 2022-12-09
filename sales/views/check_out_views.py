from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from sales.models import SellItemModel, Cart, CartItem
from sales.serializers import CartItemMiniSerializer, ProductSerializer, CartItemSerializer


class CheckoutView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get(self, request, pk, *args, **kwargs):
        ecommerce_feez = 150
        product = get_object_or_404(SellItemModel, pk=pk)
        total = ecommerce_feez + (product.price * product.quantity)
        data = {}
        data["product"] = ProductSerializer(
            product, context={"request": request}
        ).data
        data["feez"] = ecommerce_feez
        data["total"] = total

        return Response(data, status=status.HTTP_200_OK)


class CheckoutCartView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        ecommerce_feez = 150
        data = {}
        total = 0
        quantity = 0
        # user_address = Address.objects.filter(id=address_id, user=user)[0]
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            total += item.product.price
            quantity += item.quantity
        end_total = ecommerce_feez + (total * quantity)

        # data["address"] = AddressSerializer(user_address).data
        data["items"] = CartItemMiniSerializer(cart_items, many=True).data
        data["total"] = end_total
        data["feez"] = ecommerce_feez
        return Response(data, status=status.HTTP_200_OK)
