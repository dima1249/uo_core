from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django_paranoid.admin import ParanoidAdmin

from account.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# class StaticContentModelAdmin(TranslatableAdmin):
#     list_display = ('title', 'content',)
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'content',),
#         }),
#     )
#
#     def save_model(self, request, obj, form, change):
#         obj.created_by = request.user
#         super().save_model(request, obj, form, change)
#
#
from account.point_models import WatchHistoryModel


class UserModelAdmin(ParanoidAdmin, BaseUserAdmin):
    list_display = ['username', 'first_name',
                    'last_name', 'gender', 'email', 'phone', 'role']
    list_filter = ['role', 'gender', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'fb_user_id', 'google_user_id',
                     'apple_user_id']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Хувийн мэдээлэл', {'fields': (
            'first_name', 'last_name', 'gender', 'birthday')}),
        ('Нэвтрэх мэдээлэл', {'fields': (
            'dial_code', 'phone', 'email', 'fb_user_id', 'google_user_id', 'apple_user_id')}),
        ('Бусад мэдээлэл', {'fields': (
            'bank_account_number',
            'bank_account_name',
            'bank',
            'home_address',
            'id_front',
            'id_rear',
            'selfie',
            'signature')}),
        ('Онооны мэдээлэл', {'fields': (
            'point',)}),
        ('Хандалт', {'fields': (
            'is_active', 'role', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Хувийн мэдээлэл', {'fields': (
            'first_name', 'last_name', 'gender', 'birthday')}),
        ('Нэвтрэх мэдээлэл', {'fields': (
            'dial_code', 'phone', 'email', 'fb_user_id', 'google_user_id', 'apple_user_id')}),
        ('Хандалт', {'fields': (
            'is_active', 'role', 'groups', 'user_permissions')}),
    )
    readonly_fields = ['email', 'fb_user_id', 'google_user_id', 'apple_user_id', 'point']
    ordering = ['-created_at']

    # admin #agent

    def save_model(self, request, obj, form, change):
        if 'role' in request.POST:
            print(request.POST["role"])
            _code = RoleModel.objects.get(pk=request.POST["role"]).code
            print(_code)
            if "admin" == _code:
                obj.is_staff = True
                obj.is_superuser = True
            elif 'agent' == _code:
                obj.is_staff = True
                obj.is_superuser = False
            else:
                obj.is_staff = False
                obj.is_superuser = False
        obj.save()


admin.site.register(UserModel, UserModelAdmin)


class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0


admin.site.unregister(Group)


@admin.register(Group)
class GenericGroup(GroupAdmin):
    inlines = [UserInLine]
    list_display = ['name']


@admin.register(WatchHistoryModel)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('point', 'user', 'video', 'created_at',)
