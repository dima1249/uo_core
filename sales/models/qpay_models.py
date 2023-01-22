from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django_paranoid.models import ParanoidModel
from multiselectfield import MultiSelectField

from uo_core.utills import PathAndRename

max_length_id = 50
min_length_id = 20
max_length_name = 150

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

    is_company = models.BooleanField(default=False,null=True, blank=True, verbose_name="Байгууллагаар")
    company_register = models.CharField(default="",max_length=10,null=True, blank=True, verbose_name="Байгууллагын регистер")

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
        verbose_name_plural = 'Qpay invoices'
