from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from sales.models import TransactionModel, Order


@receiver(post_save, sender=TransactionModel)
def listen_charge_payment(sender, instance, *args, **kwargs):
    if instance.ref_number and instance.charge_payment_called < 1 and Order.objects.filter(
            order_number=instance.ref_number).exists():
        print('listen_charge_payment')
        _order = Order.objects.get(order_number=instance.ref_number)
        _order.to_paid = _order.to_paid + instance.amount
        _order._change_reason = "Charge payment"
        _order.save()
        _order.check_status()
        instance.charge_payment_called = instance.charge_payment_called + 1
        instance.save()
