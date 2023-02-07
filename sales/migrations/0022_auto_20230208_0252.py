# Generated by Django 3.2 on 2023-02-08 02:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0021_cartitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='in_store',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sellitemattributes',
            name='discount',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Хөнгөлөлт [%]'),
        ),
        migrations.AlterField(
            model_name='sellitemmodel',
            name='price',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Үнэ (min)'),
        ),
    ]