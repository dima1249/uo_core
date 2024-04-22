import math
import re

import requests
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, GenericAPIView
from rest_framework import permissions, status, mixins
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _

from sales.config import DELEVERY_FEEZ
from sales.models import *
from sales.serializers import CartItemSerializer, \
    CartItemUpdateSerializer, CartItemMiniSerializer

# add item
from uo_core.custom_response_utils import CustomResponse


class CartItemAPIView(ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data.get('product')
            current_item = CartItem.objects.filter(cart=cart,
                                                   product=product)

            size = serializer.validated_data.get('size')
            color = serializer.validated_data.get('color')
            _type = serializer.validated_data.get('type')
            quantity = serializer.validated_data.get('quantity')

            if _type:
                current_item = current_item.filter(type=_type)
            if color:
                current_item = current_item.filter(color=color)
            if size:
                current_item = current_item.filter(size=size)

            if current_item.count() > 0:
                raise NotAcceptable("You already have this item in your shopping cart")

            price = product.price

            attr = SellItemAttributes.objects.filter(item=product)
            if _type:
                attr = attr.filter(type=_type)
                print('attr.count()', attr.count())
            if color:
                attr = attr.filter(color=color)
                print('attr.count() color', attr.count())
            if size:
                if re.match(r'^([0-9]*[.])?[0-9]+$', size):

                    # print('attr.count()', attr[0].size, float(size))
                    attr = attr.filter(size=float(size))
                    # print('attr.count()', attr.count(), float(size))
                else:
                    attr = attr.filter(size_unit=size)
                    # print('attr.count() size_unit', attr.count())

            in_store = True

            if attr.count() > 0:
                _attr = attr.first()
                print('_attr id', _attr.id)
                if abs(_attr.quantity) < quantity:
                    raise NotAcceptable("Product quantity limit exceeds.")

                in_store = _attr.quantity > 0

                size = str(_attr.size) if _attr.size else _attr.size_unit
                color = _attr.color
                color_code = _attr.color
                atype = _attr.type

                if _attr.price and _attr.price > 0:
                    price = _attr.price

                if _attr.discount and _attr.discount > 0:
                    price = math.ceil(price * ((100 - _attr.discount) / 100.0))
            else:
                raise NotAcceptable("No Product.")

            cart_item = CartItem(cart=cart,
                                 product=product,
                                 quantity=quantity,
                                 in_store=in_store,
                                 size=size,
                                 color=color,
                                 color_code=color_code,
                                 type=_type,
                                 price=price,
                                 )
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            cart.save()
            # push_notifications(
            #     cart.user,
            #     "New cart product",
            #     "you added a product to your cart " + product.title,
            # )

            items = CartItem.objects.filter(cart=cart)
            return Response(CartItemSerializer(items, many=True).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CartClearAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.delete_cart_item()
        except Exception as e:
            print(e)

            return CustomResponse(status=False,
                                  message="Error",
                                  status_code=requests.codes.already_reported, )
        return CustomResponse(message="DONE")


# update item
class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    method_serializer_classes = {
        ('GET', 'DELETE',): CartItemSerializer,
        ('PUT',): CartItemUpdateSerializer
    }
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please, input vaild quantity")

        # if quantity > abs(cart_item.product.quantity):
        #     raise NotAcceptable("Your order quantity more than the seller have")

        if quantity == 0:
            cart_item.delete()

        serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cart_items = CartItem.objects.filter(cart=cart_item.cart)
        total = 0
        for item in cart_items:
            total += item.price * item.quantity
        end_total = total

        data = {"items": CartItemMiniSerializer(cart_items, many=True).data,
                "total": end_total, "cart_id": cart_item.cart.id,
                "feez": 0, "delevery_feez": DELEVERY_FEEZ}
        # data["address"] = AddressSerializer(user_address).data
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        cart_item.delete()
        # push_notifications(
        #     cart_item.cart.user,
        #     "deleted cart product",
        #     "you have been deleted this product: "
        #     + cart_item.product.title
        #     + " from your cart",
        # )

        return Response(
            {"detail": _("your item has been deleted.")},
            status=status.HTTP_204_NO_CONTENT,
        )
