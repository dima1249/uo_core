# Generated by Django 3.2 on 2022-11-12 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20221102_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimagemodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='image_product', to='sales.sellitemmodel', verbose_name='Зурагнууд'),
        ),
    ]
