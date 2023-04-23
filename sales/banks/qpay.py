from datetime import datetime

import requests
import time
import os
import json
import base64

from sales.models import QpayInvoiceModel, TransactionModel


class QpayV2(object):
    token = None
    token_expires = None
    _instance = None

    @staticmethod
    def get_instance():
        return QpayV2._instance if QpayV2._instance else QpayV2()

    def __init__(self):
        self.our_server = os.environ.get("OUR_HOST_URL", "http://127.0.0.1:8081")
        self.server = os.environ.get("QPAY_V2_URL")
        self.username = os.environ.get("QPAY_V2_USERNAME")
        self.password = os.environ.get("QPAY_V2_PASSWORD")
        self.invoice_code = os.environ.get("QPAY_V2_INVOICE_CODE")

    def is_valid(self):
        _last_check = time.time()
        return QpayV2.token and float(QpayV2.token_expires if QpayV2.token_expires else 0) > _last_check

    def get_token(self):
        if self.is_valid():
            return QpayV2.token
        else:
            try:
                _url = self.server + "/v2/auth/token"
                _response = requests.post(url=_url, auth=(self.username, self.password))
                if _response.status_code == requests.codes.ok:
                    _req_data = _response.json()
                    QpayV2.token = _req_data["access_token"]
                    QpayV2.token_expires = _req_data["expires_in"]
                    # print('token:', QpayV2.token)
                    # print('token_expires:', QpayV2.token_expires)
                    return QpayV2.token
                else:
                    print("qpay v2 response status code:", _response.status_code, _response.json())
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

        if total_amount < 2:
            return {"name": "ERROR", "message": "total_amount is low"}

        # if payment_type.fee and payment_type.fee > 0:
        #     total_amount = calculate_total_amount(
        #         booking_model=booking_model,
        #         fee=payment_type.fee,
        #     )

        if QpayInvoiceModel.objects.filter(ref_number=ref_number,
                                           amount=total_amount,
                                           is_paid=False).exists():

            print('already created', ref_number)
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

            order_number = ref_number
            ref_number = ref_number[:5] + str(datetime.timestamp(datetime.now()))[1:8] + ref_number[5:]
            ref_number = base64.b64encode(ref_number.encode('ascii')).decode('ascii')
            print("ref_number3", ref_number)

            # _dref_number = base64.b64decode(ref_number.encode('ascii')).decode('ascii')
            # order_number = _dref_number[:5] + _dref_number[12:]
            # print("ref_number4", order_number, _tmp, order_number == _tmp)

            try:
                call_back_url = (
                        str(self.our_server)
                        + "/api/sales/bank_check_invoicev2/"
                        + ref_number
                        + "/"
                )
                # {{end_point_local}}/api/sales/bank_check_invoicev2/UjAwMDA2ODIyMjkwMDAyMDAwMDE2MDU=

                print("call_back_url", str(call_back_url))
                _post_data = {
                    "invoice_code": str(self.invoice_code),
                    "sender_invoice_no": str(ref_number),
                    "invoice_receiver_code": "terminal",
                    "invoice_description": str(ref_number),
                    "sender_branch_code": "USUKH-OD WEB",
                    "amount": int(total_amount),
                    "callback_url": str(call_back_url),
                }

                print('create_invoice', json.dumps(_post_data))

                _url = self.server + "/v2/invoice"
                _response = requests.post(
                    url=_url, headers=self.get_header(), json=_post_data
                )
                if _response.status_code == requests.codes.ok:
                    _response_data = _response.json()
                    _qpay_invoice = QpayInvoiceModel()
                    _qpay_invoice.ref_number = order_number
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
                    _result = {"name": "ERROR"}
                    return _result
            except Exception as e:
                print("qpay error ", e)
                _result = {"name": "ERROR"}
                return _result

    def check_invoice(self, ref_number):
        _qpay_invoice_model = QpayInvoiceModel.objects.filter(
            ref_number=ref_number
        ).last()
        if _qpay_invoice_model and not _qpay_invoice_model.is_paid:
            _post_data = {
                "object_type": "INVOICE",
                "object_id": str(_qpay_invoice_model.payment_id),
                "offset": {"page_number": 1, "page_limit": 100},
            }

            _url = self.server + "/v2/payment/check"
            try:
                _response = requests.post(
                    url=_url, headers=self.get_header(), json=_post_data
                )
                if _response.status_code == requests.codes.ok:
                    _response_data = _response.json()
                    # print(_response_data)
                    if "paid_amount" in _response_data:
                        _payment_info = _response_data["rows"][0]
                        if (
                                "payment_status" in _payment_info
                                and _qpay_invoice_model.amount
                                <= float(_response_data["paid_amount"])
                        ):
                            if _payment_info["payment_status"] == "PAID":
                                if (
                                        _qpay_invoice_model.amount
                                        <= float(_payment_info["payment_amount"])
                                        and not TransactionModel.objects.filter(
                                    ref_number=_qpay_invoice_model.ref_number,
                                    payment_id=_qpay_invoice_model.payment_id,
                                ).exists()
                                ):
                                    _qpay_invoice_model.is_paid = True
                                    _qpay_invoice_model.qr_image = _response_data
                                    _qpay_invoice_model.save()
                                    _transaction = TransactionModel()
                                    _transaction.ref_number = (
                                        _qpay_invoice_model.ref_number
                                    )
                                    _transaction.payment_id = (
                                        _qpay_invoice_model.payment_id
                                    )
                                    # _transaction.payment_type = payment_type_model
                                    _transaction.transaction_type = 1
                                    if "payment_id" in _payment_info:
                                        _transaction.payment_description = (
                                            _payment_info["payment_id"]
                                        )
                                    _transaction.amount = _qpay_invoice_model.amount
                                    _transaction.save()
                                    # charge_payment(
                                    #     ref_number=_transaction.ref_number,
                                    #     amount=_transaction.amount,
                                    # )
                                    _transaction.charge_payment_called = (
                                            _transaction.charge_payment_called + 1
                                    )
                                    _transaction.save()
                                    _result = {
                                        "name": "INVOICE_PAID",
                                        "message": "INVOICE_PAID",
                                    }
                                    return _result
                                else:
                                    _result = {
                                        "name": "INVOICE_ALREADY_PAID",
                                        "message": "INVOICE_ALREADY_CREATED",
                                    }
                                    return _result
                            else:
                                _result = {
                                    "name": "INVOICE_NOT_PAID",
                                    "message": "INVOICE_NOT_PAID",
                                }
                                return _result
                        else:
                            _result = {
                                "name": "INVOICE_NOT_FOUND",
                                "message": "INVOICE_NOT_FOUND",
                            }
                            return _result
                    else:
                        _result = {
                            "name": "INVOICE_NOT_PAID",
                            "message": "INVOICE_NOT_PAID",
                        }
                        return _result
                else:
                    QpayV2.token = None
                    _result = {
                        "name": "INVOICE_NOT_PAID",
                        "message": "INVOICE_NOT_PAID",
                    }
                    return _result
            except Exception as e:
                print("qpay error: ", e)
                _result = {"name": "INVOICE_NOT_PAID", "message": "INVOICE_NOT_PAID"}
                return _result

        if _qpay_invoice_model:
            return {
                "name": "INVOICE_ALREADY_PAID",
                "message": "INVOICE_ALREADY_PAID",
            }
        return {"name": "INVOICE_NOT_FOUND", "message": "INVOICE_NOT_FOUND"}

    def cancel_invoices(self, _qpay_invoice_model):
        if not _qpay_invoice_model.is_paid:

            _url = self.server + "/v2/invoice/" + str(_qpay_invoice_model.payment_id)
            try:
                _response = requests.delete(url=_url, headers=self.get_header())
                if _response.status_code == requests.codes.ok:
                    _response_data = _response.json()

                    _qpay_invoice_model.invoice_description = "invoice_canceled"
                    _qpay_invoice_model.qr_image = str(_response_data)
                    _qpay_invoice_model.save()
                    return True

                else:
                    return False

            except Exception as e:
                return False
        return False

    def refund_invoice(self, _qpay_invoice_id):
        _qpay_invoice_model = QpayInvoiceModel.objects.filter(payment_id=_qpay_invoice_id).last()

        if _qpay_invoice_model and _qpay_invoice_model.is_paid:

            _url = self.server + "/v2/payment/refund/" + str(_qpay_invoice_model.payment_id)
            try:
                _response = requests.delete(url=_url, headers=self.get_header())
                if _response.status_code == requests.codes.ok:
                    _response_data = _response.json()

                    _qpay_invoice_model.invoice_description = "invoice refunded"
                    _qpay_invoice_model.qr_image = str(_response_data)
                    _qpay_invoice_model.save()
                    return True

                else:
                    return False

            except Exception as e:
                return False
        else:
            return False
