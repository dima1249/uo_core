from django.db import models
from django_paranoid.models import ParanoidModel

from account.models import UserModel
from sales.models import SellItemModel


class Cart(ParanoidModel):
    user = models.OneToOneField(
        UserModel, related_name="user_cart", on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )


# @receiver(post_save, sender=User)
# def create_user_cart(sender, created, instance, *args, **kwargs):
#     if created:
#         Cart.objects.create(user=instance)


class CartItem(ParanoidModel):
    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        SellItemModel, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
