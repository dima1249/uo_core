from django.contrib import admin
from django_paranoid.admin import ParanoidAdmin
from adminsortable2.admin import SortableInlineAdminMixin
from sales.models import ProductCategoryModel, BrandModel, SellItemModel, ProductImageModel, SellItemTypeModel, \
    SellItemAttributes


@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(ParanoidAdmin):
    list_display = ["name", "desc", ]


@admin.register(SellItemTypeModel)
class SellItemTypeModelAdmin(ParanoidAdmin):
    list_display = ["name", "category", "desc", ]


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


class ProductAttributesInline(admin.TabularInline):
    model = SellItemAttributes
    # readonly_fields = ["deleted_at"]
    # exclude = ["order"]
    fields = [

        "quantity",
        "type",
        "size",
        "size_unit",
        "color",
        "color_code",
    ]
    extra = 1


@admin.register(SellItemModel)
class SellItemModelAdmin(ParanoidAdmin):
    list_display = ["title", "desc", ]
    inlines = [ProductImagesInline, ProductAttributesInline]
