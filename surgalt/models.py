import datetime
from django.utils import timezone
import json

from django.db import models
from django_paranoid.models import ParanoidModel

from multiselectfield import MultiSelectField
from multiselectfield.utils import get_max_length

from account.models import GENDER, UserModel
from uo_core.utills import PathAndRename

DAY_CHOICES = ((1, 'Monday'),
               (2, 'Tuesday'),
               (3, 'Wednesday'),
               (4, 'Thursday'),
               (5, 'Friday'),
               (6, 'Sunday'),
               (7, 'Saturday'))

COURSE_CHOICES = (('A', 'Насанд хүрэгчид'),
                  ('C', 'Хүүхэд'),
                  ('S', 'Оюутан'),
                  ('O', 'Ахмад настан'),)

LEVEL_CHOICES = (('ouhm', 'Олон улс хэмжээний мастер (ОУХМ)'),
                 ('sm', 'Спортын Мастер (СМ)'),
                 ('dm', 'Спортын Мастер (ДМ)'),
                 ('level1', '1-р зэрэг'),
                 ('level2', '2-р зэрэг'),
                 ('level3', '3-р зэрэг'),
                 ('nolevel', ''),)

STATUS_CHOICES = ((1, 'Хүсэлт илгээсэн'),
                  (2, 'Төлбөр хүлээгдэж байгаа'),
                  (3, 'Бусад'),
                  (4, 'Батлагдсан'),
                  )

TEST_CHOICES = ((1, "Нэг"),
                (2, "Хоёр"),
                (3, "Гурав"),
                (4, "Дөрөв"),
                (5, "Тав"),
                (6, "Зургаа"),
                (7, "Долоо"),
                (8, "Найм"),
                (9, "Ес"),
                (10, "Арав"),)


class TeacherModel(ParanoidModel):
    firstname = models.CharField(verbose_name="Нэр", max_length=100, unique=True)
    lastname = models.CharField(verbose_name="Овог", max_length=100, blank=True, null=True)
    nick_name = models.CharField(verbose_name="Дууддаг нэр", max_length=100, blank=True, null=True)

    picture = models.ImageField(
        verbose_name="Зураг",
        upload_to=PathAndRename("teacher_pics/"),
        null=True,
        blank=True,
    )

    social = models.CharField(verbose_name="Сошиал линк", max_length=200, blank=True, null=True)

    age = models.IntegerField(verbose_name="Нас", blank=True, null=True)
    level = models.CharField(verbose_name="Спорт Зэрэг", max_length=100, default='nolevel', choices=LEVEL_CHOICES)
    story = models.TextField(verbose_name="Намтар", blank=True, null=True)

    def __str__(self):
        return '%s' % self.nick_name

    def __unicode__(self):
        return self.nick_name

    class Meta:
        db_table = 'surgalt_teachers'
        verbose_name = 'Багш'
        verbose_name_plural = 'Багш нар'


class CourseModel(ParanoidModel):
    name = models.CharField(verbose_name="Нэр", max_length=100, unique=True)
    teacher = models.ForeignKey("surgalt.TeacherModel", on_delete=models.PROTECT, verbose_name="Багш")
    picture = models.ImageField(
        verbose_name="Зураг",
        upload_to=PathAndRename("course_pics/"),
        null=True,
        blank=True,
    )
    # days = models.CharField(verbose_name="Нэр", max_length=100, unique=True)
    days = MultiSelectField(choices=DAY_CHOICES, max_choices=4, min_choices=1,
                            max_length=get_max_length(DAY_CHOICES, None))
    time = models.TimeField(verbose_name="Цаг", )
    payment = models.IntegerField(verbose_name="Төлбөр (Нэг сар)", default=0)
    is_open = models.BooleanField(verbose_name="Нээлттэй эсэх", default=True)
    type = models.CharField(verbose_name="Төрөл", choices=COURSE_CHOICES, max_length=100)
    max_student_cnt = models.IntegerField(verbose_name="Хэдэн сурагч суралцах боломжтой")
    current_student_cnt = models.IntegerField(verbose_name="Одоо суралцаж байгаа сурагч")

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'surgalt_course'
        verbose_name = 'Анги'
        verbose_name_plural = 'Анги мэдээлэл'


class CourseStudentModel(ParanoidModel):
    course = models.ForeignKey("surgalt.CourseModel", on_delete=models.PROTECT, verbose_name="Анги")
    created_user = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, verbose_name="Үүсэгсэн хэрэглэгч")
    # status = models.IntegerField(verbose_name="Төлөв", choices=STATUS_CHOICES)

    first_name = models.CharField(max_length=50, null=True, verbose_name="Нэр")
    last_name = models.CharField(max_length=50, null=True, verbose_name="Овог")
    gender = models.CharField(max_length=2, null=True, verbose_name="Хүйс", choices=GENDER)
    birthday = models.DateField(null=True, verbose_name='Төрсөн өдөр')

    start_date = models.DateField(verbose_name="Эхлэх өдөр", blank=True, null=True)
    end_date = models.DateField(verbose_name="Дуусах өдөр", blank=True, null=True)
    active = models.BooleanField(verbose_name="Идвэхтэй", default=True)
    payment_date = models.DateField(verbose_name="Төлбөр төлсөн өдөр", blank=True, null=True)
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

    def __str__(self):
        return '%s  %s - [%s]' % (self.last_name, self.first_name, self.course.name)

    def __unicode__(self):
        return '%s  %s - [%s]' % (self.last_name, self.first_name, self.course.name)

    class Meta:
        db_table = 'surgalt_course_student'
        verbose_name = 'Суралцагч'
        verbose_name_plural = 'Суралцагчид'


class StudentVideoModel(models.Model):
    student = models.ForeignKey("surgalt.CourseStudentModel", on_delete=models.PROTECT, verbose_name="Сурагч",
                                related_name='videos')
    link = models.CharField(max_length=200, null=True, verbose_name="Бичлэг линк")
    desc = models.CharField(max_length=200, null=True, verbose_name="Тайлбар")

    def __str__(self):
        return '%s - video %s' % (self.student.first_name, self.id)

    def __unicode__(self):
        return '%s - video %s' % (self.student.first_name, self.id)

    class Meta:
        db_table = 'surgalt_course_student_videos'
        verbose_name = 'Суралцагчийн бичлэг'
        verbose_name_plural = 'Суралцагчийн бичлэгнүүд'


class CourseRequestModel(ParanoidModel):
    course = models.ForeignKey("surgalt.CourseModel", on_delete=models.PROTECT, verbose_name="Анги")
    created_user = models.ForeignKey("account.UserModel", on_delete=models.PROTECT, verbose_name="Бүртгүүлэгч",
                                     default=1)

    first_name = models.CharField(max_length=50, null=True, verbose_name="Нэр")
    last_name = models.CharField(max_length=50, null=True, verbose_name="Овог")
    gender = models.CharField(max_length=2, null=True, verbose_name="Хүйс", choices=GENDER)
    birthday = models.DateField(null=True, verbose_name='Төрсөн өдөр')

    status = models.IntegerField(verbose_name="Төлөв", choices=STATUS_CHOICES, default=1)
    start_date = models.DateField(verbose_name="Эхлэх өдөр", blank=True, null=True)
    end_date = models.DateField(verbose_name="Дуусах өдөр", blank=True, null=True)
    payment_date = models.DateField(verbose_name="Төлбөр төлсөн өдөр", blank=True, null=True)
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course.name, self.first_name)

    def __unicode__(self):
        return '%s - %s' % (self.course.name, self.student.first_name)

    class Meta:
        db_table = 'surgalt_course_request'
        verbose_name = 'Анги - Бүртгэл'
        verbose_name_plural = 'Анги - Бүртгэл'

        constraints = [
            models.UniqueConstraint(fields=["course",
                                            "first_name",
                                            "last_name",
                                            "gender",
                                            "birthday",
                                            "start_date", ], name="%(app_label)s_%(class)s_unique")
        ]


class StudentTestModel(ParanoidModel):
    student = models.ForeignKey("surgalt.CourseStudentModel", on_delete=models.PROTECT, verbose_name="Суралцагч",
                                related_name='tests')

    test_date = models.DateField(verbose_name="Сургалт орсон өдөр", default=datetime.date.today)

    r1 = models.IntegerField(verbose_name="Таталт", default=5, choices=TEST_CHOICES)
    r2 = models.IntegerField(verbose_name="Тулгалт", default=5, choices=TEST_CHOICES)
    r3 = models.IntegerField(verbose_name="Топс", default=5, choices=TEST_CHOICES)
    r4 = models.IntegerField(verbose_name="Подача", default=5, choices=TEST_CHOICES)
    r5 = models.IntegerField(verbose_name="Ивэлт", default=5, choices=TEST_CHOICES)

    def __str__(self):
        return '%s - %s %s' % (self.test_date, self.student.first_name, self.student.first_name)

    def __unicode__(self):
        return '%s - %s %s' % (self.test_date, self.student.first_name, self.student.first_name)

    class Meta:
        db_table = 'surgalt_student_test'
        verbose_name = 'Суралцагч - Тест'
        verbose_name_plural = 'Суралцагч - Тест'


class StudentPointHistoryModel(ParanoidModel):
    student = models.ForeignKey("surgalt.CourseStudentModel", on_delete=models.PROTECT, verbose_name="Суралцагч",
                                related_name='point_histories')

    commit_date = models.DateTimeField(verbose_name="Огноо", default=timezone.now)

    point = models.IntegerField(verbose_name="Оноо", default=1)

    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

    def __str__(self):
        return '%s - %s %s' % (self.commit_date, self.student.first_name, self.student.first_name)

    def __unicode__(self):
        return '%s - %s %s' % (self.commit_date, self.student.first_name, self.student.first_name)

    class Meta:
        db_table = 'surgalt_student_point_history'
        verbose_name = 'Суралцагч - Оноо'
        verbose_name_plural = 'Суралцагч - Оноо'


class CourseTimeTableModel(ParanoidModel):
    course = models.ForeignKey("surgalt.CourseModel", on_delete=models.PROTECT, verbose_name="Анги")
    course_date = models.DateField(verbose_name="Сургалт орсон өдөр", default=datetime.date.today)
    desc = models.TextField(verbose_name="Тайлбар", blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course.name, self.course_date)

    def __unicode__(self):
        return '%s - %s' % (self.course.name, self.course_date)

    class Meta:
        db_table = 'surgalt_course_time_table'
        verbose_name = 'Анги - Ирц'
        verbose_name_plural = 'Анги - Ирц'


class StudentTimeTableModel(ParanoidModel):
    course_time = models.ForeignKey("surgalt.CourseTimeTableModel", on_delete=models.PROTECT, verbose_name="Хичээл")
    student = models.ForeignKey("surgalt.CourseStudentModel", on_delete=models.PROTECT, verbose_name="Суралцагч")
    attendance = models.BooleanField(verbose_name="Ирсэн", default=True)

    def __str__(self):
        return '%s - %s' % (self.student.first_name, self.course_time)

    def __unicode__(self):
        return '%s - %s' % (self.student.first_name, self.course_time)

    class Meta:
        db_table = 'surgalt_student_time_table'
        verbose_name = 'Сурагч - Ирц'
        verbose_name_plural = 'Сурагч - Ирц'
