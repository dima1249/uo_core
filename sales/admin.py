import os

from django.contrib import admin
from django_paranoid.admin import ParanoidAdmin
from adminsortable2.admin import SortableInlineAdminMixin
from django.utils.html import format_html
from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter,
    DropdownFilter,
)
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


class CartItemInline(admin.TabularInline):
    model = CartItem
    # ordering = ("order",)
    readonly_fields = ["deleted_at"]
    exclude = ["deleted_at"]
    # fields = ["title", "picture"]
    extra = 1

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Cart)
class CartAdmin(ParanoidAdmin):
    list_display = ["id", "user", "total", ]
    inlines = [CartItemInline]

    def has_change_permission(self, request, obj=None):
        return False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ["deleted_at"]
    exclude = ["deleted_at"]

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Order)
class OrderAdmin(ParanoidAdmin):
    inlines = [OrderItemInline]
    # list_filter = [("buyer", DropdownFilter),
    #                "order_number", "status", "is_paid", ]
    list_display = ["order_number", "phone", "status", "is_paid", "buyer", ]


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


#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
#     list_filter = ['available', 'created', 'updated', 'category']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}
#     inlines = [ProductImagesInline]


our_host_url = os.environ.get('OUR_HOST_URL', 'http://127.0.0.1:8081')


@admin.register(QpayInvoiceModel)
class QpayInvoiceModelAdmin(admin.ModelAdmin):
    search_fields = ["ref_number", "payment_id"]
    list_display = ["ref_number", "payment_id", "amount", "is_paid", "updated_at", "recheck"]
    readonly_fields = [
        "ref_number",
        "payment_id",
        "qpay_qr_code",
        "qpay_short_url",
        "amount",
        "currency",
        "invoice_name",
        "phone_number",
        "invoice_description",
        "qr_image",
        "deep_link",
        "is_paid",
        "is_company",
        "company_register",
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by",
        "updated_by",
        "deleted_by",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def recheck(self, obj):
        if not obj.is_paid:
            _check_button = (
                    f'<a class="button btn-primary" href="{our_host_url}/api/payment/v1/bank_check_invoicev2/'
                    + str(obj.ref_number)
                    + '/QPAY/">Check</a>&nbsp;'
            )
            return format_html(_check_button, "#")
