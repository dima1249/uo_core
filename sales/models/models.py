from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

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


class SellItemTypeModel(ParanoidModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Нэр")
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)
    category = models.ForeignKey("sales.ProductCategoryModel", on_delete=models.PROTECT, verbose_name="Төрөл", )
    picture = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Зураг",
        upload_to=PathAndRename("product_type/"), )

    def __str__(self):
        return '%s - %s' % (self.name, self.category)

    def __unicode__(self):
        return f"{self.name} - {self.category}"

    class Meta:
        db_table = 'sales_product_type'
        verbose_name = 'Бүтээгдэхүүн Төрөл'
        verbose_name_plural = 'Бүтээгдэхүүн Төрөлүүд'


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
    price = models.FloatField(default=0, verbose_name="Үнэ (min)")

    category = models.ForeignKey("sales.ProductCategoryModel", on_delete=models.PROTECT, verbose_name="Төрөл",
                                 related_name="cat_items")
    brand = models.ForeignKey("sales.BrandModel", on_delete=models.PROTECT, verbose_name="Brand",
                              related_name="brand_items")

    @property
    def total_quantity(self):
        aggregate_sum = self.attributes.aggregate(Sum('quantity'))
        return aggregate_sum.get('quantity__sum', 0) if aggregate_sum.get('quantity__sum', 0) else 0

    def __str__(self):
        return '%s (%s) [%s]' % (self.title, self.brand, self.category)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'sales_items'
        verbose_name = 'Худалдах бараа'
        verbose_name_plural = '01 Худалдах бараанууд'


class SellItemAttributes(models.Model):
    item = models.ForeignKey(SellItemModel,
                             on_delete=models.PROTECT,
                             verbose_name="Бүтээгдэхүүн",
                             related_name='attributes')
    type = models.ForeignKey(SellItemTypeModel,
                             on_delete=models.PROTECT,
                             verbose_name="Төрөл", )
    size = models.FloatField(blank=True, null=True)
    size_unit = models.CharField(max_length=20, blank=True, null=True, choices=[])
    color = models.CharField(max_length=20, blank=True, null=True, choices=[])
    color_code = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.IntegerField(default=1, verbose_name="Нийт борлуулах тоо ширхэг")
    price = models.FloatField(default=0, blank=True, null=True, verbose_name="Үнэ")

    def __str__(self):
        return '%s (%s) [%s]' % (self.item, self.type, self.id)

    def __unicode__(self):
        return self.item

    class Meta:
        unique_together = (
            "type",
            "size",
            "color",
            "quantity",
            "price",
        )
        db_table = 'sales_item_attributes'
        verbose_name = 'Бараанд харгалзах тоо ширхэг'
        verbose_name_plural = 'Бараанд харгалзах тоо ширхэг'


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
