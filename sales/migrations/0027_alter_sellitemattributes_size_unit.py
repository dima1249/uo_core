# Generated by Django 3.2 on 2023-05-30 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0026_auto_20230530_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellitemattributes',
            name='size_unit',
            field=models.CharField(choices=[('UNIT', 'UNIT'), ('S', 'S'), ('L', 'L'), ('M', 'M'), ('XL', 'XL'), ('XXL', 'XXL'), ('Q', 'Q'), ('ST', 'ST')], default='UNIT', max_length=20),
        ),
    ]
