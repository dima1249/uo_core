# Generated by Django 3.2 on 2022-12-12 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surgalt', '0005_auto_20221129_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursestudentmodel',
            name='created_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Үүсэгсэн хэрэглэгч'),
        ),
    ]
