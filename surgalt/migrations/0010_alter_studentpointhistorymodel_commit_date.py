# Generated by Django 3.2 on 2023-01-25 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surgalt', '0009_auto_20230125_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpointhistorymodel',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 25, 10, 35, 1, 685046), verbose_name='Огноо'),
        ),
    ]
