# Generated by Django 3.2 on 2022-09-22 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surgalt', '0002_auto_20220920_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursemodel',
            options={'verbose_name': 'Анги', 'verbose_name_plural': 'Анги мэдээлэл'},
        ),
        migrations.AlterModelOptions(
            name='teachermodel',
            options={'verbose_name': 'Багш', 'verbose_name_plural': 'Багш нар'},
        ),
    ]
