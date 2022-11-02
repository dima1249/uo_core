from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django_paranoid.models import ParanoidModel
from multiselectfield import MultiSelectField


class ProductCategoryModel(ParanoidModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Нэр")
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

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
    picture = models.ImageField(max_length=256, unique=True, verbose_name="Зураг")
    title = models.CharField(max_length=256, unique=True, verbose_name="Гарчиг")
    desc = models.TextField(blank=True, null=True, verbose_name="Тайлбар")

    category = models.ForeignKey("sales.ProductCategoryModel", on_delete=models.PROTECT, verbose_name="Төрөл",
                                 null=True,
                                 related_name="cat_items")
    brand = models.ForeignKey("sales.BrandModel", on_delete=models.PROTECT, verbose_name="Brand",
                              null=True,
                              related_name="brand_items")

    def __str__(self):
        return '%s' % self.title

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'sales_items'
        verbose_name = 'Худалдах бараа'
        verbose_name_plural = '01 Худалдах бараанууд'
