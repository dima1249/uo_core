import os

from django.contrib import admin, messages
from django.conf.urls import url
from django.shortcuts import redirect
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

from sales.banks.qpay import QpayV2
from sales.models import QpayInvoiceModel, TransactionModel

our_host_url = os.environ.get('OUR_HOST_URL', 'http://127.0.0.1:8081')
qpay = QpayV2.get_instance()

@admin.register(QpayInvoiceModel)
class QpayInvoiceModelAdmin(admin.ModelAdmin):
    search_fields = ["ref_number", "payment_id"]
    list_display = ["ref_number", "payment_id", "amount", "is_paid", "updated_at", "check_btn"]
    readonly_fields = [
        "ref_number",
        "payment_id",
        "qpay_qr_code",
        "qpay_short_url",
        "amount",
        "currency",
        "invoice_name",
        "phone_number",
        "invoice_description",
        "qr_image",
        "deep_link",
        "is_paid",
        "is_company",
        "company_register",
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by",
        "updated_by",
        "deleted_by",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r"^(?P<order_id>.+)/check/$",
                self.process_check,
                name="invoice_check",
            ),
        ]
        return custom_urls + urls

    def check_btn(self, obj):
        if not obj.is_paid:
            # {{end_point_local}}/api/sales/create_invoice/
            # http://127.0.0.1:8081/bff/sales/qpayinvoicemodel/
            _check_button = (
                    f'<a class="button btn-primary" href="{our_host_url}/bff/sales/qpayinvoicemodel/'
                    + str(obj.ref_number)
                    + '/check/">Check</a>&nbsp;'
            )
            return format_html(_check_button, "#")

    def process_check(self, request, order_id):
        res = qpay.check_invoice(order_id)
        print('res', res)
        if res['name'] in  ["INVOICE_PAID", "INVOICE_ALREADY_PAID"]:
            messages.add_message(
                request, messages.SUCCESS, "Төлбөр төлөгдсөн байна."
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Төлбөр төлөгдөөгүй байна."
            )
        return redirect(request.META.get("HTTP_REFERER", "/"))


#
@admin.register(TransactionModel)
class TransactionModelAdmin(SimpleHistoryAdmin):
    date_hierarchy = "created_at"
    list_filter = (
        "account_type",
        "is_hand_charge",
        "is_refunded",
    )
    search_fields = [
        "ref_number",
        "payment_id",
        "payment_type__name",
        "transaction_type",
    ]
    list_display = [
        "ref_number",
        "is_hand_charge",
        "is_refunded",
        "payment_id",
        "amount",
        "charge_payment_called",
        "updated_by",
        "transaction_type",
        "created_at",
    ]

    # readonly_fields =

    # def has_change_permission(self, request, obj=None):
    #     return False
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.payment_type:
            return [
                "ref_number",
                "amount",
                "payment_id",
                "payment_description",
                "payment_type",
                "account_type",
                "currency",
                "is_hand_charge",
                "charge_payment_called",
                "created_at",
                "updated_at",
                "deleted_at",
                "created_by",
                "updated_by",
                "deleted_by",
            ]
        elif obj and obj.is_hand_charge:
            return [
                "ref_number",
                "amount",
                "payment_id",
                "payment_description",
                "payment_type",
                "account_type",
                "currency",
                "is_hand_charge",
                "charge_payment_called",
                "created_at",
                "updated_at",
                "deleted_at",
                "created_by",
                "updated_by",
                "deleted_by",
            ]
        else:
            return [
                "payment_id",
                "is_refunded",
                "payment_type",
                "account_type",
                "currency",
                "is_hand_charge",
                "charge_payment_called",
                "created_at",
                "updated_at",
                "deleted_at",
                "created_by",
                "updated_by",
                "deleted_by",
            ]

    def save_model(self, request, obj, form, change):
        try:
            obj.updated_by = request.user
            if obj.created_by is None:
                obj.created_by = request.user
            obj._change_reason = (
                    str(obj.ref_number)
                    + " "
                    + str(obj.amount)
                    + " MNT "
                    + str(obj.transaction_type)
            )
            obj.save()
        except AttributeError as e:
            print(e)
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
