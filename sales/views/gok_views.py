import os
import random
from datetime import datetime
from django.http import HttpResponse
from rest_framework import permissions, exceptions, status, serializers, viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListCreateAPIView, CreateAPIView, mixins

from sales.banks.qpay import QpayV2
from sales.models import *

from sales.serializers.order_serializers import OrderSerializer, CreateOrderSerializer
from sales.utils import time_calculator

qpay = QpayV2.get_instance()


class CreateInvoiceSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    order_number = serializers.CharField(
        min_length=3,
        required=True, help_text="Захиалгын давтагдашгүй код"
    )


class CreateInvoiceView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateInvoiceSerializer

    # serializer_class = OrderSerializer

    @time_calculator
    def time(self):
        return 0

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_number = serializer.data.get("order_number")

            item = Order.objects.filter(order_number=order_number).first()
            if item:
                order_serializer = OrderSerializer(item)
                print("order_serializer ", order_serializer.data)
                _result = qpay.create_invoice(
                    order_number, order_serializer.data.get('to_pay', 1)
                )
                print("qpay.create_invoice _result ", _result)

                if "name" in _result and _result["name"] == "ERROR":
                    return Response("error", status=status.HTTP_208_ALREADY_REPORTED)
                return Response(_result, status=status.HTTP_201_CREATED)
            raise serializers.ValidationError(
                "Not Found"
            )
        return Response(serializer.errors, status=status.HTTP_208_ALREADY_REPORTED)


class BankCheckInvoiceV2(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateInvoiceSerializer

    # @csrf_protect
    def list(self, request, *args, **kwargs):

        if "ref_number" in kwargs:

            _ref_number = kwargs["ref_number"]
            _booking_model = None
            # _booking_model = GokProvider.get_booking_model_without_status(_ref_number=_ref_number)

            if _booking_model:
                _response_data = qpay.check_invoice(
                    booking_model=_booking_model
                )

                if _response_data["name"] in ["INVOICE_PAID", "INVOICE_ALREADY_PAID"]:
                    return HttpResponse("done")
                else:
                    return HttpResponse("undone")
            else:
                return HttpResponse("undone")

        else:
            return HttpResponse("undone")

    # @csrf_protect
    def create(self, request, *args, **kwargs):

        if "ref_number" in kwargs and "payment_type" in kwargs:
            _ref_number_temp = kwargs["ref_number"]
            _ref_number = _ref_number_temp.split("K")[0]
            payment_type_name = kwargs["payment_type"]
        #     _booking_model = GokProvider.get_booking_model_without_status(_ref_number=_ref_number)
        #
        #     if _booking_model:
        #         if _booking_model.status != 1:
        #             MailMessage.warring_bank_check_order(_ref_number=_ref_number, payment_type=payment_type_name)
        #
        #         payment_type = PaymentTypeModel.objects.filter(
        #             name=payment_type_name
        #         ).first()
        #         if payment_type and payment_type.name == "QPAY":
        #             _response_data = qpay.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "HIPAY":
        #             _response_data = hipay.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "XACBANK":
        #             _response_data = xacbank.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "TDB":
        #             _response_data = tdb.check_invoice_and_confirm(
        #                 booking_model=_booking_model,
        #                 payment_type_model=payment_type,
        #                 request=request,
        #             )
        #         elif payment_type and payment_type.name == "GOLOMT":
        #             _response_data = golomt.check_invoice(
        #                 booking_model=_booking_model, ref_number_temp=_ref_number_temp, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "STATEBANK":
        #             _response_data = statebank.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "STRIPE":
        #             _response_data = _stripe.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "CRYPTOCOM":
        #             _response_data = crypto_com.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "PASSMN":
        #             _response_data = pass_mn.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #         elif payment_type and payment_type.name == "MONPAY":
        #             _response_data = monpay.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #
        #         elif payment_type and payment_type.name == "KHANBANK":
        #             _response_data = khanbank.check_invoice(
        #                 booking_model=_booking_model, payment_type_model=payment_type
        #             )
        #
        #         else:
        #             _ctx = {
        #                 "response_title": gsms.PAYMENT_NOT_FOUND,
        #                 "response_pic": AWS_S3_CUSTOM_DOMAIN
        #                                 + "/media/paymentstatus/unsuccessful.png",
        #                 "response_description": "",
        #             }
        #             _body = get_template("payment_response.html").render(_ctx)
        #             return HttpResponse(_body)
        #
        #         if _response_data["name"] == "INVOICE_PAID":
        #             # segment.payment_invoice(
        #             #     request=None,
        #             #     api_url="payment/v1/bank_check_invoice/get",
        #             #     booking=_booking_model,
        #             #     payment=payment_type,
        #             # )
        #             _ctx = {
        #                 "response_title": gsms.PAYMENT_SUCCESS,
        #                 "response_pic": AWS_S3_CUSTOM_DOMAIN + "/media/paymentstatus/successful.png",
        #                 "response_description": str(gsms.PAYMENT_SUCCESS_DESCRIPTION)
        #                                         + " "
        #                                         + str(_booking_model.to_pay)
        #                                         + " MNT",
        #             }
        #             _body = get_template("payment_response.html").render(_ctx)
        #             mail_title = _ref_number + " " + str(gsms.ORDER_PAYMENT_PAID)
        #             _message_body = (
        #                     "TAPATRIP.COM "
        #                     + str(_booking_model.ref_number)
        #                     + " Payment successfully: "
        #                     + str(_booking_model.to_pay)
        #                     + " MNT"
        #             )
        #             # send_mail_message(to_mail=_booking_model.contact_email, dial_nubmer=_booking_model.contact_dial_number,
        #             #                   phone=_booking_model.contact_phone,
        #             #                   mail_title=mail_title, mail_body=_body, message_body=_message_body)
        #             return HttpResponse(_body)
        #         elif _response_data["name"] == "INVOICE_ALREADY_PAID":
        #             _ctx = {
        #                 "response_title": gsms.PAYMENT_SUCCESS,
        #                 "response_pic": AWS_S3_CUSTOM_DOMAIN + "/media/paymentstatus/successful.png",
        #                 "response_description": str(gsms.PAYMENT_SUCCESS_DESCRIPTION)
        #                                         + " "
        #                                         + str(_booking_model.to_pay)
        #                                         + " MNT",
        #             }
        #             _body = get_template("payment_response.html").render(_ctx)
        #             return HttpResponse(_body)
        #         else:
        #             _ctx = {
        #                 "response_title": gsms.PAYMENT_UNSUCCESS,
        #                 "response_pic": AWS_S3_CUSTOM_DOMAIN
        #                                 + "/media/paymentstatus/unsuccessful.png",
        #                 "response_description": gsms.PAYMENT_UNSUCCESS_DESCRIPTION,
        #             }
        #             _body = get_template("payment_response.html").render(_ctx)
        #             return HttpResponse(_body)
        #     else:
        #         MailMessage.warring_bank_check_order(_ref_number=_ref_number, payment_type=payment_type_name)
        #         _ctx = {
        #             "response_title": gsms.PAYMENT_ORDER_NOT_FOUND,
        #             "response_pic": AWS_S3_CUSTOM_DOMAIN + "/media/paymentstatus/unsuccessful.png",
        #             "response_description": "",
        #         }
        #         _body = get_template("payment_response.html").render(_ctx)
        #         return HttpResponse(_body)
        #
        # else:
        #     _ctx = {
        #         "response_title": gsms.PAYMENT_ORDER_NOT_FOUND,
        #         "response_pic": AWS_S3_CUSTOM_DOMAIN + "/media/paymentstatus/unsuccessful.png",
        #         "response_description": "",
        #     }
        #     _body = get_template("payment_response.html").render(_ctx)
        #     return HttpResponse(_body)


class CheckInvoice(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateInvoiceSerializer

    def create(self, request, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            _ref_number = serializer.data.get("ref_number")
            # _booking_model = GokProvider.get_booking_model_without_status(
            #     _ref_number=_ref_number
            # )
            #
            # if _booking_model:
            _response_data = qpay.check_invoice(
                booking_model=_booking_model
            )

            if _response_data["name"] == "INVOICE_PAID":
                # _ctx = {
                #     "response_title": gsms.PAYMENT_SUCCESS,
                #     "response_pic": AWS_S3_CUSTOM_DOMAIN
                #     + "/media/paymentstatus/successful.png",
                #     "response_description": str(gsms.PAYMENT_SUCCESS_DESCRIPTION)
                #     + " "
                #     + str(_booking_model.to_pay)
                #     + " MNT",
                # }
                # _body = get_template("payment_response.html").render(_ctx)
                # mail_title = _ref_number + " " + str(gsms.ORDER_PAYMENT_PAID)
                # _message_body = (
                #     "TAPATRIP.COM "
                #     + str(_booking_model.ref_number)
                #     + " Payment successfully: "
                #     + str(_booking_model.to_pay)
                #     + " MNT"
                # )
                # send_mail_message(to_mail=_booking_model.contact_email,
                #                   dial_nubmer=_booking_model.contact_dial_number,
                #                   phone=_booking_model.contact_phone,
                #                   mail_title=mail_title, mail_body=_body, message_body=_message_body)
                return Response(_response_data, status=status.HTTP_200_OK)

            elif _response_data["name"] == "INVOICE_ALREADY_PAID":
                # _ctx = {
                #     "response_title": gsms.PAYMENT_SUCCESS,
                #     "response_pic": AWS_S3_CUSTOM_DOMAIN
                #     + "/media/paymentstatus/successful.png",
                #     "response_description": str(gsms.PAYMENT_SUCCESS_DESCRIPTION)
                #     + " "
                #     + str(_booking_model.to_pay)
                #     + " MNT",
                # }
                # _body = get_template("payment_response.html").render(_ctx)
                return Response(_response_data, status=status.HTTP_202_ACCEPTED)

            else:
                return Response(_response_data, status=status.HTTP_208_ALREADY_REPORTED)

        return Response("error", status=status.HTTP_406_NOT_ACCEPTABLE)
