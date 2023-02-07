# Generated by Django 3.2 on 2023-02-01 13:42

from django.db import migrations, models
import django.db.models.deletion
import uo_core.utills


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0014_historicaltransactionmodel_transactionmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellitemmodel',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='sellitemmodel',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='brand_items', to='sales.brandmodel', verbose_name='Brand'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sellitemmodel',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='cat_items', to='sales.productcategorymodel', verbose_name='Төрөл'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sellitemmodel',
            name='price',
            field=models.FloatField(default=0, verbose_name='Үнэ (min)'),
        ),
        migrations.CreateModel(
            name='SellItemTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Нэр')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=uo_core.utills.PathAndRename('product_type/'), verbose_name='Зураг')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.productcategorymodel', verbose_name='Төрөл')),
            ],
            options={
                'verbose_name': 'Бүтээгдэхүүн Төрөл',
                'verbose_name_plural': 'Бүтээгдэхүүн Төрөлүүд',
                'db_table': 'sales_product_type',
            },
        ),
        migrations.CreateModel(
            name='SellItemAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.FloatField(blank=True, null=True)),
                ('size_unit', models.CharField(blank=True, choices=[], max_length=20, null=True)),
                ('color', models.CharField(blank=True, choices=[], max_length=20, null=True)),
                ('color_code', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.IntegerField(default=1, verbose_name='Нийт борлуулах тоо ширхэг')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Үнэ')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attributes', to='sales.sellitemmodel', verbose_name='Бүтээгдэхүүн')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.sellitemtypemodel', verbose_name='Төрөл')),
            ],
            options={
                'verbose_name': 'Бараанд харгалзах тоо ширхэг',
                'verbose_name_plural': 'Бараанд харгалзах тоо ширхэг',
                'db_table': 'sales_item_attributes',
                'unique_together': {('type', 'size', 'color', 'quantity', 'price')},
            },
        ),
    ]