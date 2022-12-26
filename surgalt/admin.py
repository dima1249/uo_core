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

    list_filter = [("course", DropdownFilter),
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


@admin.register(CourseStudentModel)
class CourseStudentModelAdmin(ParanoidAdmin):
    list_display = ["course", "created_user", "active", "start_date", "end_date", ]
    list_filter = ["course", "created_user", "active",]
    ordering = ["course", "active", "start_date", "end_date",]


@admin.register(StudentTestModel)
class StudentTestModelAdmin(ParanoidAdmin):
    list_display = ["course", "student", "test_date", ]


class StudentTimeTableInline(admin.TabularInline):
    model = StudentTimeTableModel
    exclude = ["deleted_at"]
    extra = 1


@admin.register(CourseTimeTableModel)
class CourseTimeTableModelAdmin(ParanoidAdmin):
    list_display = ["course", "course_date"]

    inlines = [StudentTimeTableInline]
