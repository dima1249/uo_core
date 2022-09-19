from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django_paranoid.models import ParanoidModel
from multiselectfield import MultiSelectField


class VideoCategoryModel(ParanoidModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Нэр")
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sales_video_cat'
        verbose_name = 'Үзвэрийн ангилал'
        verbose_name_plural = 'Үзвэрийн ангилалууд'


class VideoModel(ParanoidModel):
    link_to_connect = models.CharField(max_length=256, unique=True, verbose_name="Холбогдох холбоос")
    video_link = models.CharField(max_length=256, unique=True, verbose_name="Үзвэрийн холбоос(Youtube)")
    loyalty_amount = models.FloatField(verbose_name="Урамшууллын үнэ")
    length = models.IntegerField(blank=True, null=True, verbose_name="Үзвэр урт")
    watch_limit = models.IntegerField(blank=True, null=True, verbose_name="Үзвэр Үзэх хязгаар")
    # users = models.ManyToManyField(User, verbose_name="Үзсэн хэрэглэгчид")
    # time_table = MultiSelectField(choices=TIME_TABLE, verbose_name='Нислэгийн хуваарь', null=True, blank=True)
    desc = models.TextField(blank=True, null=True, verbose_name="Тайлбар")

    host_name = models.CharField(max_length=100, verbose_name="Эзэмшэгчийн нэр", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Content name", default="default")

    category = models.ForeignKey("sales.VideoCategoryModel", on_delete=models.PROTECT, verbose_name="Төрөл", null=True,
                             related_name="cat_videos")

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sales_video'
        verbose_name = 'Видео Үзвэр'
        verbose_name_plural = 'Видео Үзвэрүүд'


class VideoTimeModel(models.Model):
    video = models.ForeignKey("sales.VideoModel", on_delete=models.PROTECT, verbose_name="check time",
                              related_name="video_check")
    duration = models.IntegerField(verbose_name="check minute", null=True, blank=True)

    def __str__(self):
        return '%s' % self.duration

    def __unicode__(self):
        return self.duration

    class Meta:
        db_table = 'sales_video_time'
        verbose_name = 'Шалгах Хугацаа'
        verbose_name_plural = 'Шалгах Хугацаанууд'


class VideoWatchModel(models.Model):
    video = models.ForeignKey("sales.VideoModel", on_delete=models.PROTECT, verbose_name="check time",
                              related_name="watch_video")

    user = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, verbose_name="check time",
                             related_name="watch_user")

    def __str__(self):
        return '%s %s' % (self.video.id, self.user.id)

    def __unicode__(self):
        return '%s %s' % (self.video.id, self.user.id)

    class Meta:
        db_table = 'sales_video_watch'
        verbose_name = 'Үзвэр ба хэрэглэгч'
        verbose_name_plural = 'Үзвэр ба хэрэглэгчид'
