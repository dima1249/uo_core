# Generated by Django 3.2 on 2022-10-26 00:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import uo_core.utills


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Нэр')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=uo_core.utills.PathAndRename('course_pics/'), verbose_name='Зураг')),
                ('days', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Sunday'), (7, 'Saturday')], max_length=13)),
                ('time', models.TimeField(verbose_name='Цаг')),
                ('payment', models.IntegerField(default=0, verbose_name='Төлбөр (Нэг сар)')),
                ('is_open', models.BooleanField(default=True, verbose_name='Нээлттэй эсэх')),
                ('type', models.CharField(choices=[('A', 'Насанд хүрэгчид'), ('C', 'Хүүхэд'), ('S', 'Оюутан'), ('O', 'Ахмад настан')], max_length=100, verbose_name='Төрөл')),
                ('max_student_cnt', models.IntegerField(verbose_name='Хэдэн сурагч суралцах боломжтой')),
                ('current_student_cnt', models.IntegerField(verbose_name='Одоо суралцаж байгаа сурагч')),
            ],
            options={
                'verbose_name': 'Анги',
                'verbose_name_plural': 'Анги мэдээлэл',
                'db_table': 'surgalt_course',
            },
        ),
        migrations.CreateModel(
            name='CourseTimeTableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('course_date', models.DateField(default=datetime.date.today, verbose_name='Сургалт орсон өдөр')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surgalt.coursemodel', verbose_name='Анги')),
            ],
            options={
                'verbose_name': 'Анги - Ирц',
                'verbose_name_plural': 'Анги - Ирц',
                'db_table': 'surgalt_course_time_table',
            },
        ),
        migrations.CreateModel(
            name='TeacherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('firstname', models.CharField(max_length=100, unique=True, verbose_name='Нэр')),
                ('lastname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Овог')),
                ('nick_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Дууддаг нэр')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Нас')),
                ('level', models.CharField(choices=[('ouhm', 'Олон улс хэмжээний мастер (ОУХМ)'), ('sm', 'Спортын Мастер (СМ)'), ('dm', 'Спортын Мастер (ДМ)'), ('level1', '1-р зэрэг'), ('level2', '2-р зэрэг'), ('level3', '3-р зэрэг'), ('nolevel', '')], default='nolevel', max_length=100, verbose_name='Спорт Зэрэг')),
                ('story', models.TextField(blank=True, null=True, verbose_name='Намтар')),
            ],
            options={
                'verbose_name': 'Багш',
                'verbose_name_plural': 'Багш нар',
                'db_table': 'surgalt_teachers',
            },
        ),
        migrations.CreateModel(
            name='StudentTimeTableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('attendance', models.BooleanField(default=True, verbose_name='Ирсэн')),
                ('course_time', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surgalt.coursetimetablemodel', verbose_name='Хичээл')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Суралцагч')),
            ],
            options={
                'verbose_name': 'Сурагч - Ирц',
                'verbose_name_plural': 'Сурагч - Ирц',
                'db_table': 'surgalt_student_time_table',
            },
        ),
        migrations.CreateModel(
            name='StudentTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('test_date', models.DateField(default=datetime.date.today, verbose_name='Сургалт орсон өдөр')),
                ('r1', models.IntegerField(choices=[(1, 'Нэг'), (2, 'Хоёр'), (3, 'Гурав'), (4, 'Дөрөв'), (5, 'Тав'), (6, 'Зургаа'), (7, 'Долоо'), (8, 'Найм'), (9, 'Ес'), (10, 'Арав')], default=5, verbose_name='Таталт')),
                ('r2', models.IntegerField(choices=[(1, 'Нэг'), (2, 'Хоёр'), (3, 'Гурав'), (4, 'Дөрөв'), (5, 'Тав'), (6, 'Зургаа'), (7, 'Долоо'), (8, 'Найм'), (9, 'Ес'), (10, 'Арав')], default=5, verbose_name='Тулгалт')),
                ('r3', models.IntegerField(choices=[(1, 'Нэг'), (2, 'Хоёр'), (3, 'Гурав'), (4, 'Дөрөв'), (5, 'Тав'), (6, 'Зургаа'), (7, 'Долоо'), (8, 'Найм'), (9, 'Ес'), (10, 'Арав')], default=5, verbose_name='Топс')),
                ('r4', models.IntegerField(choices=[(1, 'Нэг'), (2, 'Хоёр'), (3, 'Гурав'), (4, 'Дөрөв'), (5, 'Тав'), (6, 'Зургаа'), (7, 'Долоо'), (8, 'Найм'), (9, 'Ес'), (10, 'Арав')], default=5, verbose_name='Подача')),
                ('r5', models.IntegerField(choices=[(1, 'Нэг'), (2, 'Хоёр'), (3, 'Гурав'), (4, 'Дөрөв'), (5, 'Тав'), (6, 'Зургаа'), (7, 'Долоо'), (8, 'Найм'), (9, 'Ес'), (10, 'Арав')], default=5, verbose_name='Ивэлт')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surgalt.coursemodel', verbose_name='Анги')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Суралцагч')),
            ],
            options={
                'verbose_name': 'Анги - Тест',
                'verbose_name_plural': 'Анги - Тест',
                'db_table': 'surgalt_student_test',
            },
        ),
        migrations.CreateModel(
            name='CourseStudentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Эхлэх өдөр')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дуусах өдөр')),
                ('active', models.BooleanField(default=True, verbose_name='Идвэхтэй')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='Төлбөр төлсөн өдөр')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surgalt.coursemodel', verbose_name='Анги')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Суралцагч')),
            ],
            options={
                'verbose_name': 'Анги - Сурагч',
                'verbose_name_plural': 'Анги - Сурагч',
                'db_table': 'surgalt_course_student',
            },
        ),
        migrations.CreateModel(
            name='CourseRequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Хүсэлт илгээсэн'), (2, 'Төлбөр хүлээгдэж байгаа'), (3, 'Бусад'), (3, 'Батлагдсан')], default=1, verbose_name='Төлөв')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Эхлэх өдөр')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дуусах өдөр')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='Төлбөр төлсөн өдөр')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surgalt.coursemodel', verbose_name='Анги')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Суралцагч')),
            ],
            options={
                'verbose_name': 'Анги - Бүртгэл',
                'verbose_name_plural': 'Анги - Бүртгэл',
                'db_table': 'surgalt_course_request',
            },
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surgalt.teachermodel', verbose_name='Багш'),
        ),
    ]
