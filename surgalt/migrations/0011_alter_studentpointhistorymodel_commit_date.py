# Generated by Django 3.2 on 2023-01-25 10:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surgalt', '0010_alter_studentpointhistorymodel_commit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpointhistorymodel',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 25, 10, 42, 41, 674572), verbose_name='Огноо'),
        ),
    ]