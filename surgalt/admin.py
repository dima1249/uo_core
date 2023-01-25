from django.contrib import admin
from django_paranoid.admin import ParanoidAdmin

from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter,
    DropdownFilter,
)

from surgalt.models import *


@admin.register(TeacherModel)
class TeacherModelAdmin(ParanoidAdmin):
    list_display = ["firstname", "lastname", ]


@admin.register(CourseModel)
class CourseModelAdmin(ParanoidAdmin):
    list_display = ["name", "type", ]


@admin.register(CourseRequestModel)
class CourseRequestModelAdmin(ParanoidAdmin):
    list_display = ["course", "student_info", "status", "created_at"]
    readonly_fields = ["created_user", "deleted_at"]

    list_filter = [
        ("course"),
        # ("created_user", DropdownFilter),
        "created_user", ]

    fieldsets = (
        (None, {'fields': ('status',)}),
        ('Хувийн мэдээлэл', {'fields': (
            'first_name', 'last_name', 'gender', 'birthday')}),
        ('Анги мэдээлэл', {'fields': (
            'course', 'start_date', 'end_date')}),
        ('Бусад', {'fields': (
            'payment_date', 'desc')}),
    )

    def student_info(self, obj):
        return f"{obj.last_name} {obj.first_name} ({obj.gender})"

    student_info.short_description = "Суралцагч"


class StudentVideoInline(admin.TabularInline):
    model = StudentVideoModel
    extra = 1


class StudentPointInline(admin.StackedInline):
    model = StudentPointHistoryModel
    readonly_fields = ['deleted_at', 'commit_date']

    show_change_link = False
    extra = 0
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(CourseStudentModel)
class CourseStudentModelAdmin(ParanoidAdmin):
    list_display = ["course", "created_user", "active", "start_date", "end_date", ]
    list_filter = ["course", "created_user", "active", ]
    search_fields = ['first_name', 'last_name']
    ordering = ["course", "active", "start_date", "end_date", ]
    inlines = [StudentVideoInline,
               StudentPointInline ]

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj=None) \
               + ("created_user", "active")

    fieldsets = (
        (None, {'fields': ('active', 'created_user',)}),
        ('Хувийн мэдээлэл', {'fields': (
            'first_name', 'last_name', 'gender', 'birthday')}),
        ('Сургалт Хугацаа', {'fields': (
            'course', 'start_date', 'end_date', 'payment_date')}),
        ('Бусад', {'fields': (
            'desc',)}),
        # ('Бичлэг', {'fields': (
        #     'desc',)}),
    )


@admin.register(StudentTestModel)
class StudentTestModelAdmin(ParanoidAdmin):
    list_display = ["student", "test_date", ]
    autocomplete_fields = ["student"]


@admin.register(StudentPointHistoryModel)
class StudentPointHistoryAdmin(ParanoidAdmin):
    list_display = ["student", "commit_date", "point"]
    autocomplete_fields = ["student"]

    def get_readonly_fields(self, request, obj=None):
        return super().readonly_fields + ("commit_date",)

    def has_delete_permission(self, request, obj=None):
        return False


class StudentTimeTableInline(admin.TabularInline):
    model = StudentTimeTableModel
    exclude = ["deleted_at"]
    extra = 1


@admin.register(CourseTimeTableModel)
class CourseTimeTableModelAdmin(ParanoidAdmin):
    list_display = ["course", "course_date"]

    inlines = [StudentTimeTableInline]
