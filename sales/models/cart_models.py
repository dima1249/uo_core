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


@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    print("receiver create_user_cart")
    if created:
        Cart.objects.create(user=instance)


class CartItem(ParanoidModel):
    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        SellItemModel, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
