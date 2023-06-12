from django.db import models
from django.db.models import Sum
from django_paranoid.models import ParanoidModel
from simple_history.models import HistoricalRecords

from account.models import UserModel

# uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
# created = models.DateTimeField(auto_now_add=True, db_index=True)
# modified = models.DateTimeField(auto_now=True)
from sales.models import SellItemModel


class Address(ParanoidModel):
    # user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    # country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    # phone_number = PhoneNumberField(null=True, blank=True)
    building_number = models.IntegerField(
        blank=True, null=True
    )
    apartment_number = models.IntegerField(
        blank=True, null=True
    )


class Order(ParanoidModel):
    PENDING_STATE = "p"
    COMPLETED_STATE = "o"
    CANCELED_STATE = "c"

    ORDER_CHOICES = ((PENDING_STATE, "Pending"), (COMPLETED_STATE, "Completed"), (CANCELED_STATE, "Canceled"))

    buyer = models.ForeignKey(UserModel, related_name="order", on_delete=models.CASCADE)
    order_number = models.CharField(max_length=250, blank=True, null=True)
    firstname = models.CharField(max_length=250, default="", null=True)
    lastname = models.CharField(max_length=250, default="", null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    delivery = models.BooleanField(default=True)
    status = models.CharField(
        max_length=1, choices=ORDER_CHOICES, default=PENDING_STATE
    )
    is_paid = models.BooleanField(default=False)
    to_paid = models.FloatField(default=0, verbose_name='Төлөгдсөн дүн')
    address = models.ForeignKey(
        Address, related_name="order_address", on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        db_table = 'sales_orders'
        verbose_name = 'Захиалга'
        verbose_name_plural = '02 Захиалганууд'

    def __str__(self):
        return self.order_number

    def __unicode__(self):
        return self.order_number

    def check_status(self):
        to_pay = self.to_pay()
        if not self.is_paid and to_pay <= self.to_paid:
            self.is_paid = True
            self.status = self.COMPLETED_STATE
            self.save()
            print("payment completed")
        else:
            print(F"payment {self.to_paid} > {to_pay}")
            print("payment incomplete")

    def to_pay(self):
        to_pay = self.order_items.aggregate(Sum('total')).get('total__sum', 0)
        return int(to_pay) if to_pay else 0
        # return int(to_pay) if to_pay else 0

    @staticmethod
    def create_order(buyer, order_number, phone,
                     delivery,
                     address="",
                     firstname='',
                     lastname='',
                     is_paid=False):
        order = Order()
        order.buyer = buyer
        order.order_number = order_number
        # order.address = address
        order.firstname = firstname
        order.lastname = lastname
        order.phone = phone
        order.delivery = delivery
        order.is_paid = is_paid
        order.save()
        return order


class OrderItem(ParanoidModel):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        SellItemModel, related_name="product_order", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sales_order_items'
        verbose_name = 'Захиалганд харгалзах бараа'
        verbose_name_plural = 'Захиалганд харгалзах бараанууд'

    @staticmethod
    def create_order_item(order, product, quantity, total):
        order_item = OrderItem()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        order_item.total = total
        order_item.save()
        return order_item
