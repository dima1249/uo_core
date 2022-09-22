from django_paranoid.models import ParanoidModel
from django.db import models
from multiselectfield import MultiSelectField

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


class TeacherModel(ParanoidModel):
    firstname = models.CharField(verbose_name="Нэр", max_length=100, unique=True)
    lastname = models.CharField(verbose_name="Овог", max_length=100, blank=True, null=True)
    nick_name = models.CharField(verbose_name="Дууддаг нэр", max_length=100, blank=True, null=True)

    age = models.IntegerField(verbose_name="Нас", blank=True, null=True)
    level = models.CharField(verbose_name="Спорт Зэрэг",  max_length=100, default='nolevel', choices=LEVEL_CHOICES)
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
    # days = models.CharField(verbose_name="Нэр", max_length=100, unique=True)
    days = MultiSelectField(choices=DAY_CHOICES, max_choices=4, min_choices=1)
    time = models.TimeField(verbose_name="Цаг", )
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