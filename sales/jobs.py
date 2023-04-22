from datetime import datetime, timedelta

from sales.banks.qpay import QpayV2
from sales.models import QpayInvoiceModel


qpay = QpayV2.get_instance()

class FetchInvoiceClass:
    def run(self):
        pass

    def check_invoice(self):
        QpayInvoiceModel.objects.filter('')

        check_time = datetime.now() - timedelta(minutes=119)

        qpay_invoices = QpayInvoiceModel.objects.filter(is_paid=False, created_at__lte=check_time)
        print('qpay_invoices', len(qpay_invoices))
        # for qpay_invoice in qpay_invoices:
        #     qpay.cancel_invoices(qpay_invoice)

