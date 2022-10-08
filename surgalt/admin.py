from django.contrib import admin

# Register your models here.
from django_paranoid.admin import ParanoidAdmin

from surgalt.models import *


@admin.register(TeacherModel)
class TeacherModelAdmin(ParanoidAdmin):
    list_display = ["firstname", "lastname", ]


@admin.register(CourseModel)
class CourseModelAdmin(ParanoidAdmin):
    list_display = ["name", "type", ]


@admin.register(CourseRequestModel)
class CourseRequestModelAdmin(ParanoidAdmin):
    list_display = ["course", "student", "status", "created_at", ]


@admin.register(CourseStudentModel)
class CourseStudentModelAdmin(ParanoidAdmin):
    list_display = ["course", "student", "active", "start_date", "end_date", ]


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
