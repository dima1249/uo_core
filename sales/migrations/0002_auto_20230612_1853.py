# Generated by Django 3.2 on 2023-06-12 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='firstname',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='lastname',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='firstname',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='lastname',
            field=models.CharField(default='', max_length=250, null=True),
        ),
    ]
