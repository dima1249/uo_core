from django.contrib import admin

# Register your models here.
from django_paranoid.admin import ParanoidAdmin

from sales.models import VideoModel, VideoTimeModel, VideoCategoryModel


class VideoTimeModelInline(admin.StackedInline):
    model = VideoTimeModel
    extra = 1
    exclude = ['deleted_at']


@admin.register(VideoModel)
class VideoModelAdmin(ParanoidAdmin):
    list_display = ["name", "loyalty_amount", "video_link", "desc", ]
    inlines = [VideoTimeModelInline]


@admin.register(VideoCategoryModel)
class VideoCategoryAdmin(ParanoidAdmin):
    list_display = ["name", "desc"]
