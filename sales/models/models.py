from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django_paranoid.models import ParanoidModel
from multiselectfield import MultiSelectField

from uo_core.utills import PathAndRename


class ProductCategoryModel(ParanoidModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Нэр")
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)
    picture = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Зураг",
        upload_to=PathAndRename("product_categories/"), )

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sales_product_cat'
        verbose_name = 'Бүтээгдэхүүн ангилал'
        verbose_name_plural = 'Бүтээгдэхүүн ангилалууд'


class BrandModel(ParanoidModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Нэр")
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sales_brand'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class SellItemModel(ParanoidModel):
    title = models.CharField(max_length=256, unique=True, verbose_name="Гарчиг")
    desc = models.TextField(blank=True, null=True, verbose_name="Тайлбар")
    price = models.FloatField(default=0, blank=True, null=True, verbose_name="Үнэ")
    quantity = models.IntegerField(default=1, blank=True, null=True, verbose_name="Нийт борлуулах тоо ширхэг")

    category = models.ForeignKey("sales.ProductCategoryModel", on_delete=models.PROTECT, verbose_name="Төрөл",
                                 null=True,
                                 related_name="cat_items")
    brand = models.ForeignKey("sales.BrandModel", on_delete=models.PROTECT, verbose_name="Brand",
                              null=True,
                              related_name="brand_items")

    def __str__(self):
        return '%s (%s) [%s]' % (self.title, self.brand, self.category)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'sales_items'
        verbose_name = 'Худалдах бараа'
        verbose_name_plural = '01 Худалдах бараанууд'


# class SellItemSizeAttributes(models.Model):
#     item = models.ForeignKey(SellItemModel)
#     attr_value = models.IntegerField()


class ProductImageModel(models.Model):
    title = models.CharField(blank=True, null=True, default='Picture', max_length=100, verbose_name="Зураг гарчиг")
    picture = models.ImageField(
        verbose_name="Зураг",
        upload_to=PathAndRename("product_pics/"), )
    product = models.ForeignKey("sales.SellItemModel", on_delete=models.PROTECT, verbose_name="Зурагнууд",
                                null=True,
                                related_name="image_product")

    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name="эрэмбэ"
    )

    def __str__(self):
        return '%s' % self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']
        db_table = 'sales_item_picture'
        verbose_name = 'Худалдах барааны зурагнууд'
        # verbose_name_plural = '01 Худалдах бараанууд'
