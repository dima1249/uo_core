# Generated by Django 3.2 on 2022-12-27 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('p', 'Pending'), ('o', 'Completed'), ('c', 'Canceled')], default='p', max_length=1),
        ),
    ]
