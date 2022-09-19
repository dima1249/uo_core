import datetime
import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.utils import timezone
from django_paranoid.models import ParanoidModel

GENDER = (
    ("F", "F"),  #
    ("M", "M"),  #
    ("FI", "FI"),  #
    ("MI", "MI"),  #
    ("U", "U"),  #
    ("X", "X"),  #
)


class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = UserModel()
        user.username = username
        user.email = 'no-reply@mail.tapatrip.com'
        # user.user_type = AGENT
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

        # def get_by_natural_key(self, email_):
        #     return self.get(email=email_)


class RoleModel(ParanoidModel):
    name = models.CharField(max_length=200, verbose_name="Role-ийн нэр")
    code = models.CharField(max_length=200, verbose_name="Role-ийн код")

    def __str__(self):
        return '%s' % self.name


BANKS = [
    ("KHAN", "Хаан банк"),
    ("GOLOMT", "Голомт банк"),
    ("STATE", "Төрийн банк"),
]


class UserModel(ParanoidModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, verbose_name="Нэвтрэх нэр")
    # display_name = models.CharField(max_length=50, null=True, verbose_name="Дэлгэцэнд харуулах нэр")
    first_name = models.CharField(max_length=50, null=True, verbose_name="Нэр")
    last_name = models.CharField(max_length=50, null=True, verbose_name="Овог")
    gender = models.CharField(max_length=2, null=True, verbose_name="Хүйс", choices=GENDER)
    profile_picture = models.CharField(max_length=200, null=True, verbose_name="Зураг")
    birthday = models.DateField(null=True, verbose_name='Төрсөн өдөр')

    # gadnii hereglegchiig odoohondoo tootsoogui tul max_length-g 11-r(976-99999999) avav
    dial_code = models.CharField(verbose_name="Утасны код", max_length=3, null=True, blank=True)
    phone = models.CharField(verbose_name="Утасны дугаар", max_length=11, null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name="И-мэйл хаяг", null=True, blank=True)

    fb_user_id = models.CharField(max_length=100, verbose_name="facebook user id", null=True, blank=True)
    google_user_id = models.CharField(max_length=200, verbose_name="google user id", null=True, blank=True)
    apple_user_id = models.CharField(max_length=200, verbose_name="apple user id", null=True, blank=True)

    role = models.ForeignKey("account.RoleModel", on_delete=models.PROTECT, verbose_name="role", null=True)

    is_active = models.BooleanField(default=True, verbose_name="Идэвхитэй эсэх")
    is_staff = models.BooleanField(default=False, verbose_name="Ажилтан эсэх")

    # other field

    point = models.FloatField(default=0, null=True, blank=True, verbose_name="Оноо")

    bank_account_number = models.CharField(verbose_name="Данс дугаар", max_length=20, null=True, blank=True)
    bank_account_name = models.CharField(verbose_name="Данс нэр", max_length=20, null=True, blank=True)
    bank = models.CharField(verbose_name="Банк", default="KHAN",
                            choices=BANKS,
                            max_length=10)

    home_address = models.CharField(verbose_name="Гэрийн хаяг", max_length=256, null=True, blank=True)

    id_front = models.ImageField(verbose_name="Иргэний үнэмлэх урд тал", max_length=256, null=True, blank=True)
    id_rear = models.ImageField(verbose_name="Иргэний үнэмлэх ард тал", max_length=256, null=True, blank=True)
    signature = models.ImageField(verbose_name="Гарын үсэг", max_length=256, null=True, blank=True)
    selfie = models.ImageField(verbose_name="Зураг", max_length=256, null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        if self.email and len(self.email):
            return '%s' % self.email
        return '%s' % self.username

    def __unicode__(self):
        if self.email and len(self.email):
            return '%s' % self.email
        return '%s' % self.username

    class Meta:
        db_table = 'users'
        verbose_name = 'Хэрэглэгч'
        verbose_name_plural = 'Хэрэглэгчид'


# Холбогдсон төхөөрөмжийн бүтэц


class DeviceModel(ParanoidModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, verbose_name="Хэрэглэгч", null=True,
                             related_name="device_settings_user")
    device_ip = models.CharField(
        max_length=16, verbose_name='Төхөөрөмжийн IP хаяг')
    device_name = models.CharField(
        max_length=200, verbose_name='Төхөөрөмжийн нэр')
    device_os = models.CharField(
        max_length=200, verbose_name='Төхөөрөмжийн үйлдэлийн систем')
    device_based_token = models.CharField(
        max_length=200, verbose_name='Төхөөрөмжөөр үүсгэсэн токен', null=True, blank=True)

    class Meta:
        db_table = 'devices_connected'
        verbose_name = 'Холбогдсон төхөөрөмж'
        verbose_name_plural = 'Холбогдсон төхөөрөмжүүд'


# class StaticContentModel(ParanoidModel):
#     title = models.CharField(verbose_name="Title", max_length=200, unique=True),
#     content = models.CharField(verbose_name="Content", max_length=200, unique=True),
#     code = models.CharField(max_length=200, null=True)
#     created_by = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='user_static_content')
#
#     class Meta:
#         db_table = 'static_content'
#         verbose_name = "Cтатик контент"
#         verbose_name_plural = "Cтатик контентууд"


# class StaticContentModelTranslation(TranslatedFieldsModel):
#     master = models.ForeignKey(StaticContentModel, related_name='translations', on_delete=models.PROTECT, null=True)
#     title = models.CharField(_("Title"), max_length=200, null=True)
#     content = RichTextField(null=True)
#
#     class Meta:
#         db_table = 'static_content_translation'
#         # verbose_name = _("static_content_translation")
#         verbose_name = _("StaticContentModel translation")


class VerificationCodeModel(ParanoidModel):
    dial_code = models.CharField(verbose_name="Утасны код", null=True, blank=True, max_length=3)
    phone = models.CharField(verbose_name="Утасны дугаар", max_length=11, null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name="И-мэйл хаяг", null=True, blank=True)
    code = models.CharField(max_length=6, verbose_name='Баталгаажуулах код')
    send_sms_time = models.DateTimeField(verbose_name="sms илгээсэн хугацаа")
    is_verify = models.BooleanField(default=False)
    try_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="Оролдсон тоо")

    @property
    def is_active(self):
        time = self.send_sms_time + datetime.timedelta(minutes=5)
        if timezone.now() < time:
            return True
        return False

    @property
    def is_confirm(self):
        time = self.updated_at + datetime.timedelta(days=1)
        if timezone.now() > time:
            return False

        if self.is_verify:
            return True

        return False

    class Meta:
        db_table = 'notify_verification_codes'
        verbose_name = 'Баталгаажуулах код'
        verbose_name_plural = 'Баталгаажуулах кодууд'
