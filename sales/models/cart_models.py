from django.db import models
from django_paranoid.models import ParanoidModel
from django.dispatch import receiver

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from sales.models import SellItemModel, colors, SellItemTypeModel

User = get_user_model()


class Cart(ParanoidModel):
    user = models.OneToOneField(
        User, related_name="user_cart", on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )

    def __str__(self):
        return '%s' % self.user

    def __unicode__(self):
        return self.user

    def check_product_quantity(self):
        if self.cart_items.count() == 0:
            return True
        return False

    class Meta:
        db_table = 'sales_carts'
        verbose_name = 'Сагс'
        verbose_name_plural = 'Сагснууд'

    def delete_cart_item(self):
        print("deleted cart_items")
        self.cart_items.all().delete()


@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    # print("receiver create_user_cart")
    if created:
        Cart.objects.create(user=instance)


class CartItem(ParanoidModel):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        SellItemModel, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    in_store = models.BooleanField(default=True)
    size = models.CharField(max_length=5, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True, choices=colors)
    color_code = models.CharField(max_length=20, blank=True, null=True, choices=colors)
    type = models.ForeignKey(SellItemTypeModel,
                             on_delete=models.PROTECT,
                             verbose_name="Загвар",
                             blank=True, null=True)

    price = models.FloatField(default=0, verbose_name='Ширхэг үнэ')

    def __str__(self):
        return '%s' % self.product

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'sales_cart_item'
        verbose_name = 'Сагсан дахь бараа'
        verbose_name_plural = 'Сагсан дахь бараанууд'
