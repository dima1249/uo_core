from django.db import models
from django_paranoid.models import ParanoidModel
from simple_history.models import HistoricalRecords

max_length_id = 50
min_length_id = 20
max_length_name = 150

TRANSACTION_TYPE = [
    (1, 'ОРЛОГО'),
    (2, 'ЗАРЛАГА'),
]


class QpayInvoiceModel(ParanoidModel):
    ref_number = models.CharField(max_length=max_length_id, null=True, blank=True, verbose_name="ref number")
    payment_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Payment id")
    qpay_qr_code = models.TextField(null=True, blank=True, verbose_name="QPAY QR code")
    qpay_short_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="QPAY short ulr")
    amount = models.FloatField(default=0, null=True, blank=True, verbose_name="мөнгөн дүн")
    currency = models.CharField(default="MNT", max_length=10, null=True, blank=True, verbose_name="Мөнгөн тэмдэгт")

    invoice_name = models.CharField(max_length=max_length_name, null=True, blank=True, verbose_name="invoice name")
    phone_number = models.CharField(max_length=max_length_name, null=True, blank=True, verbose_name="phone")
    invoice_description = models.CharField(max_length=200, null=True, blank=True, verbose_name="invoice discription")
    qr_image = models.TextField(null=True, blank=True, verbose_name="qr image")
    deep_link = models.TextField(null=True, blank=True, verbose_name="deeplinks")

    is_paid = models.BooleanField(default=False, null=True, blank=True, verbose_name="Төлөгдсөн")

    is_company = models.BooleanField(default=False, null=True, blank=True, verbose_name="Байгууллагаар")
    company_register = models.CharField(default="", max_length=10, null=True, blank=True,
                                        verbose_name="Байгууллагын регистер")

    created_by = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Үүсгэсэн хэрэглэгч", related_name="created_qpay_user")
    updated_by = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Шинэчилсэн хэрэглэгч", related_name="updated_qpay_user")
    deleted_by = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Устгасан хэрэглэгч", related_name="deleted_qpay_user")

    def __str__(self):
        return '%s' % self.ref_number

    def __unicode__(self):
        return self.ref_number

    class Meta:
        db_table = 'sales_qpay_invoice'
        verbose_name = 'Qpay invoice'
        verbose_name_plural = 'B3 Qpay invoices'


class TransactionModel(ParanoidModel):
    ref_number = models.CharField(max_length=max_length_id, null=True, blank=True, verbose_name="ref number")
    payment_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Payment id")
    # payment_type = models.ForeignKey("gok.PaymentTypeModel", on_delete=models.PROTECT, null=True, blank=True,
    #                                  verbose_name="Гүйлгээний хийсэн банк")
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True, blank=True,
                                           verbose_name="Гүйлгээний төрөл")

    payment_description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Гүйлгээний утга")
    amount = models.FloatField(default=0, null=True, blank=True, verbose_name="Үнэ")
    currency = models.CharField(default="MNT", max_length=10, null=True, blank=True, verbose_name="Мөнгөн тэмдэгт")
    account_type = models.CharField(max_length=20, null=True, blank=True, verbose_name="Данс эзэмшигчийн ҮА чиглэл")
    is_refunded = models.BooleanField(default=0, null=True, blank=True, verbose_name="Төлбөр буцаасан")
    is_hand_charge = models.BooleanField(default=0, null=True, blank=True, verbose_name="Гараар нэмсэн")
    charge_payment_called = models.IntegerField(default=0, null=True, blank=True, verbose_name="charged count")

    created_by = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Үүсгэсэн хэрэглэгч", related_name="created_transaction_user")
    updated_by = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Шинэчилсэн хэрэглэгч", related_name="updated_transaction_user")
    deleted_by = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Устгасан хэрэглэгч", related_name="deleted_transaction_user")

    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.ref_number

    def __unicode__(self):
        return self.ref_number

    class Meta:
        db_table = 'gok_transaction'
        verbose_name = 'Transaction'
        verbose_name_plural = 'B2 Transactions'
