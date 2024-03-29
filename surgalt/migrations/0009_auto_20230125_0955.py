# Generated by Django 3.2 on 2023-01-25 09:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surgalt', '0008_auto_20230123_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursestudentmodel',
            options={'verbose_name': 'Суралцагч', 'verbose_name_plural': 'Суралцагчид'},
        ),
        migrations.AlterModelOptions(
            name='studenttestmodel',
            options={'verbose_name': 'Суралцагч - Тест', 'verbose_name_plural': 'Суралцагч - Тест'},
        ),
        migrations.CreateModel(
            name='StudentPointHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('commit_date', models.DateTimeField(default=datetime.date.today, verbose_name='Огноо')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('point', models.IntegerField(default=1, verbose_name='Оноо')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='point_histories', to='surgalt.coursestudentmodel', verbose_name='Суралцагч')),
            ],
            options={
                'verbose_name': 'Суралцагч - Оноо',
                'verbose_name_plural': 'Суралцагч - Оноо',
                'db_table': 'surgalt_student_point_history',
            },
        ),
    ]
