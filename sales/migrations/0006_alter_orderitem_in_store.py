# Generated by Django 3.2 on 2024-04-23 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20240414_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='in_store',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
