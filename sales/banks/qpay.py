import requests
import time
from datetime import datetime
import os
import json

from django.core.cache import cache

from sales.models import QpayInvoiceModel


class QpayV2(object):
    token = None
    token_expires = None

    def __init__(self):
        self.our_server = os.environ.get("OUR_HOST_URL")
        self.server = os.environ.get("QPAY_V2_URL")
        self.username = os.environ.get("QPAY_V2_USERNAME")
        self.password = os.environ.get("QPAY_V2_PASSWORD")
        self.invoice_code = os.environ.get("QPAY_V2_INVOICE_CODE")

    def is_valid(self):
        _last_check = time.time()
        return cache.get("QPAY_TOKEN") and float(cache.get("QPAY_EXPIRES_IN")) > _last_check

    def get_token(self):
        if self.is_valid():
            return cache.get("QPAY_TOKEN")
        else:
            try:
                _url = self.server + "/v2/auth/token"
                _response = requests.post(url=_url, auth=(self.username, self.password))
                if _response.status_code == requests.codes.ok:
                    _req_data = _response.json()
                    cache.delete("QPAY_TOKEN")
                    cache.delete("QPAY_EXPIRES_IN")
                    QpayV2.token = _req_data["access_token"]
                    QpayV2.token_expires = _req_data["expires_in"]
                    cache.set("QPAY_EXPIRES_IN", QpayV2.token_expires, timeout=None)
                    cache.set("QPAY_TOKEN", QpayV2.token, timeout=None)
                    return cache.get("QPAY_TOKEN")
                else:
                    print("qpay v2 response status code:", _response.status_code, _response.json())
                    cache.delete("QPAY_TOKEN")
                    QpayV2.token = None
                    return None
            except Exception as e:
                print("qpay token error", e)
                return False

    def get_header(self):
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.get_token()),
        }
        return header

    def create_invoice(self, ref_number, to_pay):
        total_amount = to_pay

        # if payment_type.fee and payment_type.fee > 0:
        #     total_amount = calculate_total_amount(
        #         booking_model=booking_model,
        #         fee=payment_type.fee,
        #     )

        if QpayInvoiceModel.objects.filter(ref_number=ref_number,
                                           amount=total_amount,
                                           is_paid=False).exists():

            _qpay_invoice = QpayInvoiceModel.objects.filter(
                ref_number=ref_number, amount=total_amount, is_paid=False
            ).last()
            _result = {"qPay_QRcode": _qpay_invoice.qpay_qr_code, "payment_id": _qpay_invoice.payment_id,
                       "qPay_url": _qpay_invoice.qpay_short_url, "qPay_shortUrl": _qpay_invoice.qpay_short_url,
                       "qPay_QRimage": _qpay_invoice.qr_image, "qPay_deeplink": json.loads(_qpay_invoice.deep_link)}
            return _result

        elif QpayInvoiceModel.objects.filter(
                ref_number=ref_number, is_paid=True
        ).exists():
            _result = {
                "name": "INVOICE_ALREADY_CREATED",
                "message": "INVOICE_ALREADY_CREATED",
            }
            return _result
        else:

            try:
                call_back_url = (
                        str(self.our_server)
                        + "/api/payment/v1/bank_check_invoicev2/"
                        + ref_number
                        + "/QPAY/"
                )
                _post_data = {
                    "invoice_code": str(self.invoice_code),
                    "sender_invoice_no": str(ref_number),
                    "invoice_receiver_code": "terminal",
                    "invoice_description": str(ref_number),
                    "sender_branch_code": "TAPATRIP RIVER",
                    "amount": int(total_amount),
                    "callback_url": str(call_back_url),
                }

                _url = self.server + "/v2/invoice"
                _response = requests.post(
                    url=_url, headers=self.get_header(), json=_post_data
                )
                if _response.status_code == requests.codes.ok:
                    _response_data = _response.json()
                    _qpay_invoice = QpayInvoiceModel()
                    _qpay_invoice.ref_number = ref_number
                    _qpay_invoice.amount = total_amount
                    _qpay_invoice.invoice_name = ref_number
                    _qpay_invoice.invoice_description = ref_number
                    _qpay_invoice.phone_number = "86224468"
                    if "invoice_id" in _response_data:
                        _qpay_invoice.payment_id = _response_data["invoice_id"]
                    if "qr_text" in _response_data:
                        _qpay_invoice.qpay_qr_code = _response_data["qr_text"]
                    if "qPay_shortUrl" in _response_data:
                        _qpay_invoice.qpay_short_url = _response_data["qPay_shortUrl"]
                    if "qr_image" in _response_data:
                        _qpay_invoice.qr_image = _response_data["qr_image"]
                    if "urls" in _response_data:
                        _qpay_invoice.deep_link = json.dumps(_response_data["urls"])
                    _qpay_invoice.save()

                    _result = {"qPay_QRcode": _qpay_invoice.qpay_qr_code,
                               "payment_id": _qpay_invoice.payment_id,
                               "qPay_url": _qpay_invoice.qpay_short_url,
                               "qPay_shortUrl": _qpay_invoice.qpay_short_url,
                               "qPay_QRimage": _qpay_invoice.qr_image,
                               "qPay_deeplink": _response_data["urls"]}
                    return _result
                else:
                    print("qpay v2 response status code:", _response.status_code, _response.json())
                    QpayV2.token = None
                    cache.delete("QPAY_TOKEN")
                    cache.delete("QPAY_EXPIRES_IN")
                    _result = {"name": "ERROR"}
                    return _result
            except Exception as e:
                print("qpay error ", e)
                _result = {"name": "ERROR"}
                return _result
    #
    # def check_invoice(self, booking_model, payment_type_model):
    #     total_amount = booking_model.to_pay
    #     if payment_type_model.fee and payment_type_model.fee > 0:
    #         total_amount = calculate_total_amount(
    #             booking_model=booking_model,
    #             fee=payment_type_model.fee,
    #         )
    #     _qpay_invoice_model = QpayInvoiceModel.objects.filter(
    #         ref_number=booking_model.ref_number, is_paid=False
    #     ).last()
    #     if _qpay_invoice_model:
    #         _post_data = {
    #             "object_type": "INVOICE",
    #             "object_id": str(_qpay_invoice_model.payment_id),
    #             "offset": {"page_number": 1, "page_limit": 100},
    #         }
    #
    #         _url = self.server + "/v2/payment/check"
    #         try:
    #             _response = requests.post(
    #                 url=_url, headers=self.get_header(), json=_post_data
    #             )
    #             if _response.status_code == requests.codes.ok:
    #                 _response_data = _response.json()
    #                 # print(_response_data)
    #                 if "paid_amount" in _response_data:
    #                     _payment_info = _response_data["rows"][0]
    #                     if (
    #                         "payment_status" in _payment_info
    #                         and _qpay_invoice_model.amount
    #                         <= float(_response_data["paid_amount"])
    #                     ):
    #                         if _payment_info["payment_status"] == "PAID":
    #                             if (
    #                                 _qpay_invoice_model.amount
    #                                 <= float(_payment_info["payment_amount"])
    #                                 and not TransactionModel.objects.filter(
    #                                     ref_number=_qpay_invoice_model.ref_number,
    #                                     payment_id=_qpay_invoice_model.payment_id,
    #                                 ).exists()
    #                             ):
    #                                 _qpay_invoice_model.is_paid = True
    #                                 _qpay_invoice_model.qr_image = _response_data
    #                                 _qpay_invoice_model.save()
    #                                 _transaction = TransactionModel()
    #                                 _transaction.ref_number = (
    #                                     _qpay_invoice_model.ref_number
    #                                 )
    #                                 _transaction.payment_id = (
    #                                     _qpay_invoice_model.payment_id
    #                                 )
    #                                 _transaction.payment_type = payment_type_model
    #                                 _transaction.transaction_type = 1
    #                                 if "payment_id" in _payment_info:
    #                                     _transaction.payment_description = (
    #                                         _payment_info["payment_id"]
    #                                     )
    #                                 _transaction.amount = _qpay_invoice_model.amount
    #                                 _transaction.save()
    #                                 charge_payment(
    #                                     ref_number=_transaction.ref_number,
    #                                     amount=_transaction.amount,
    #                                 )
    #                                 _transaction.charge_payment_called = (
    #                                     _transaction.charge_payment_called + 1
    #                                 )
    #                                 _transaction.save()
    #                                 _result = {
    #                                     "name": "INVOICE_PAID",
    #                                     "message": gsms.INVOICE_PAID,
    #                                 }
    #                                 return _result
    #                             else:
    #                                 _result = {
    #                                     "name": "INVOICE_ALREADY_PAID",
    #                                     "message": gsms.INVOICE_ALREADY_CREATED,
    #                                 }
    #                                 return _result
    #                         else:
    #                             _result = {
    #                                 "name": "INVOICE_NOT_PAID",
    #                                 "message": gsms.INVOICE_NOT_PAID,
    #                             }
    #                             return _result
    #                     else:
    #                         _result = {
    #                             "name": "INVOICE_NOT_FOUND",
    #                             "message": gsms.INVOICE_NOT_FOUND,
    #                         }
    #                         return _result
    #                 else:
    #                     _result = {
    #                         "name": "INVOICE_NOT_PAID",
    #                         "message": gsms.INVOICE_NOT_PAID,
    #                     }
    #                     return _result
    #             else:
    #                 QpayV2.token = None
    #                 _result = {
    #                     "name": "INVOICE_NOT_PAID",
    #                     "message": gsms.INVOICE_NOT_PAID,
    #                 }
    #                 return _result
    #         except Exception as e:
    #             print("qpay error: ", e)
    #             _result = {"name": "INVOICE_NOT_PAID", "message": gsms.INVOICE_NOT_PAID}
    #             return _result
    #     elif QpayInvoiceModel.objects.filter(
    #         ref_number=booking_model.ref_number, is_paid=True
    #     ).exists():
    #         _result = {
    #             "name": "INVOICE_ALREADY_PAID",
    #             "message": gsms.INVOICE_ALREADY_PAID,
    #         }
    #         return _result
    #     else:
    #         _result = {"name": "INVOICE_NOT_FOUND", "message": gsms.INVOICE_NOT_FOUND}
    #         return _result
    #
    # def cancel_invoices(self, _qpay_invoice_model):
    #
    #     if not _qpay_invoice_model.is_paid:
    #
    #         _url = self.server + "/v2/invoice/" + str(_qpay_invoice_model.payment_id)
    #         try:
    #             _response = requests.delete(url=_url, headers=self.get_header())
    #             if _response.status_code == requests.codes.ok:
    #                 _response_data = _response.json()
    #
    #                 _qpay_invoice_model.invoice_description = "invoice_canceled"
    #                 _qpay_invoice_model.qr_image = str(_response_data)
    #                 _qpay_invoice_model.save()
    #                 return True
    #
    #             else:
    #                 return False
    #
    #         except Exception as e:
    #             return False
    #     return False
    #
    # def refund_invoice(self, _qpay_invoice_id):
    #     _qpay_invoice_model = QpayInvoiceModel.objects.filter(payment_id=_qpay_invoice_id).last()
    #
    #     if _qpay_invoice_model and _qpay_invoice_model.is_paid:
    #
    #         _url = self.server + "/v2/payment/refund/" + str(_qpay_invoice_model.payment_id)
    #         try:
    #             _response = requests.delete(url=_url, headers=self.get_header())
    #             if _response.status_code == requests.codes.ok:
    #                 _response_data = _response.json()
    #
    #                 _qpay_invoice_model.invoice_description = "invoice refunded"
    #                 _qpay_invoice_model.qr_image = str(_response_data)
    #                 _qpay_invoice_model.save()
    #                 return True
    #
    #             else:
    #                 return False
    #
    #         except Exception as e:
    #             return False
    #     else:
    #         return False
