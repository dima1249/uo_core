from django.db import models
from django_paranoid.models import ParanoidModel
from django.dispatch import receiver

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from sales.models import SellItemModel

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
        for item in self.cart_items.all():
            if item.product.quantity < item.quantity:
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

    def __str__(self):
        return '%s' % self.product

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'sales_cart_item'
        verbose_name = 'Сагсан дахь бараа'
        verbose_name_plural = 'Сагсан дахь бараанууд'
