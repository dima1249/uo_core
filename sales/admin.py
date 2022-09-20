from django.contrib import admin

# Register your models here.
from django_paranoid.admin import ParanoidAdmin
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
    list_display = ["name",  "desc", ]

@admin.register(BrandModel)
class BrandModelAdmin(ParanoidAdmin):
    list_display = ["name",  "desc", ]

@admin.register(SellItemModel)
class SellItemModelAdmin(ParanoidAdmin):
    list_display = ["title",  "desc", ]
