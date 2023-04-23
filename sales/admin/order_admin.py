from django.contrib import admin
from django_paranoid.admin import ParanoidAdmin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

from sales.models import *


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
    autocomplete_fields = ["user", ]
    search_fields = ["user"]
    list_filter = [
        ("user"),
        # ("user", DropdownFilter),
    ]

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
    list_filter = [ "status", "is_paid", ]
    # autocomplete_fields = ["order_number",]
    search_fields = ['order_number']
    list_display = ["order_number", "phone", "status", "col_payment", "buyer", ]

    readonly_fields = ['order_number', 'buyer', 'is_paid', 'to_paid', 'deleted_at']

    date_hierarchy = "created_at"

    empty_value_display = "-empty-"

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(
        description="Төлбөр",
        ordering="to_paid",
    )
    def col_payment(self, obj):

        return f"{obj.to_paid:,} - {obj.to_pay():,}"