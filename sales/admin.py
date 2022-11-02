from django.contrib import admin
from django_paranoid.admin import ParanoidAdmin
from adminsortable2.admin import SortableInlineAdminMixin
from sales.models import *


#
#
# class VideoTimeModelInline(admin.StackedInline):
#     model = VideoTimeModel
#     extra = 1
#     exclude = ['deleted_at']
#
#
@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(ParanoidAdmin):
    list_display = ["name", "desc", ]


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

#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
#     list_filter = ['available', 'created', 'updated', 'category']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}
#     inlines = [ProductImagesInline]
