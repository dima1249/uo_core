from django.db import models
from django.db.models import Sum
from django_paranoid.models import ParanoidModel
from simple_history.models import HistoricalRecords
from account.models import UserModel
from sales.models import SellItemModel, SellItemTypeModel


DELIVERY_FEE = 5000


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
    address = models.TextField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'sales_orders'
        verbose_name = 'Захиалга'
        verbose_name_plural = 'B1 Захиалганууд'

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
        to_pay = (int(to_pay) if to_pay else 0) + (DELIVERY_FEE if self.delivery else 0)

        return to_pay
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
        order.address = address
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

    in_store = models.BooleanField(default=True, null=True)
    size = models.CharField(max_length=5, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    color_code = models.CharField(max_length=20, blank=True, null=True)


    price = models.FloatField(default=0, blank=True, null=True, verbose_name='Ширхэг үнэ')

    type = models.ForeignKey(SellItemTypeModel,
                             on_delete=models.PROTECT,
                             verbose_name="Загвар",
                             blank=True, null=True)

    class Meta:
        db_table = 'sales_order_items'
        verbose_name = 'Захиалганд харгалзах бараа'
        verbose_name_plural = 'Захиалганд харгалзах бараанууд'

    @staticmethod
    def create_order_item(order, cartItem):
        order_item = OrderItem()
        order_item.order = order
        order_item.product = cartItem.product
        order_item.quantity = cartItem.quantity
        order_item.total = cartItem.quantity * cartItem.price

        order_item.in_store = cartItem.in_store
        order_item.size = cartItem.size
        order_item.color = cartItem.color
        order_item.color_code = cartItem.color_code
        order_item.type = cartItem.type
        order_item.price = cartItem.price
        # type
        # price
        order_item.save()
        return order_item
