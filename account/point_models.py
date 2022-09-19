import datetime
from django.db import models

# Create your models here.
from django.utils import timezone
from django_paranoid.models import ParanoidModel

from sales.models import VideoModel


class WatchHistoryModel(ParanoidModel):
    point = models.FloatField(default=0, null=True, blank=True, verbose_name="Оноо")
    user = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, verbose_name="Хэрэглэгч", null=True,
                             related_name="history_user")
    video = models.ForeignKey("sales.VideoModel", on_delete=models.PROTECT, verbose_name="Үзвэр", null=True,
                              related_name="history_video")

    def __str__(self):
        return '%s' % self.id

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'watch_histories'
        verbose_name = 'Түүх'
        verbose_name_plural = 'Үзсэн түүхүүд'

    @staticmethod
    def save_history(user, video_id):
        video = VideoModel.objects.get(id=video_id)
        user.point = user.point + video.loyalty_amount
        user.save()
        item = WatchHistoryModel()
        item.point = video.loyalty_amount
        item.user = user
        item.video = video
        item.save()


class TransactionModel(ParanoidModel):
    bank_account_number = models.CharField(verbose_name="Утасны дугаар", max_length=20, null=True, blank=True)
    bank_account_name = models.CharField(verbose_name="Утасны дугаар", max_length=20, null=True, blank=True)
    bank = models.CharField(verbose_name="Утасны дугаар", max_length=20, null=True, blank=True)
    status = models.CharField(verbose_name="Статус", max_length=20, null=True, blank=True)

    point = models.IntegerField(default=0, null=True, blank=True, verbose_name="Оноо")
    user = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, verbose_name="Хэрэглэгч", null=True,
                             related_name="transaction_user")

    class Meta:
        db_table = 'point_transaction'
        verbose_name = 'Гүйлгээ'
        verbose_name_plural = 'Гүйлгээнүүд'
