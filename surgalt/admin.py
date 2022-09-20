from django.contrib import admin

# Register your models here.
from django_paranoid.admin import ParanoidAdmin

from surgalt.models import *


@admin.register(TeacherModel)
class TeacherModelAdmin(ParanoidAdmin):
    list_display = ["firstname",  "lastname", ]

@admin.register(CourseModel)
class CourseModelAdmin(ParanoidAdmin):
    list_display = ["name",  "type", ]