from django.contrib import admin
from django_paranoid.admin import ParanoidAdmin
from adminsortable2.admin import SortableInlineAdminMixin
from sales.models import ProductCategoryModel, BrandModel, SellItemModel, ProductImageModel


@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(ParanoidAdmin):
    list_display = ["name", "desc", ]


# GENERAL
@admin.register(BrandModel)
class BrandModelAdmin(ParanoidAdmin):
    list_display = ["name", "desc", ]


class ProductImagesInline(admin.TabularInline, SortableInlineAdminMixin):
    model = ProductImageModel
    ordering = ("order",)
    # readonly_fields = ["deleted_at"]
    exclude = ["order"]
    fields = ["title", "picture"]
    extra = 1


@admin.register(SellItemModel)
class SellItemModelAdmin(ParanoidAdmin):
    list_display = ["title", "desc", ]
    inlines = [ProductImagesInline]
