from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django_paranoid.admin import ParanoidAdmin

from account.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(ParanoidAdmin, BaseUserAdmin):
    list_display = ['email', 'col_fullname', 'gender', 'phone',  'email', 'role']
    list_filter = ['role', 'gender', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'fb_user_id', 'google_user_id',
                     'apple_user_id']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Хувийн мэдээлэл', {'fields': (
            'first_name', 'last_name', 'gender', 'birthday')}),
        ('Нэвтрэх мэдээлэл', {'fields': (
            'dial_code', 'phone', 'email', 'verify_code', 'fb_user_id', 'google_user_id', 'apple_user_id')}),
        # ('Бусад мэдээлэл', {'fields': (
        #     'bank_account_number',
        #     'bank_account_name',
        #     'bank',
        #     'home_address',
        #     'id_front',
        #     'id_rear',
        #     'selfie',
        #     'signature')}),
        # ('Онооны мэдээлэл', {'fields': (
        #     'point',)}),
        ('Хандалт', {'fields': (
            'is_active', 'is_staff', 'role', 'groups', 'user_permissions')}),
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
    readonly_fields = ['email', 'verify_code', 'fb_user_id', 'google_user_id', 'apple_user_id']
    ordering = ['-created_at']

    @admin.display(
        description="Нэр",
        ordering="first_name")
    def col_fullname(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    # admin #agent

    def save_model(self, request, obj, form, change):
        if 'role' in request.POST:
            print(request.POST["role"])
            _code = RoleModel.objects.get(pk=request.POST["role"]).code
            print(_code)
            if "admin" == _code:
                obj.is_staff = True
                obj.is_superuser = True
            elif 'teacher' == _code:
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


@admin.register(RoleModel)
class RoleModelGroup(ParanoidAdmin):
    def has_delete_permission(self, request, obj=None):
        return not bool(obj and obj.id < 3)

    def has_change_permission(self, request, obj=None):
        return not bool(obj and obj.id <= 4)
