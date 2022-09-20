# Generated by Django 3.2.12 on 2022-09-20 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrandModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Нэр')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'db_table': 'sales_brand',
            },
        ),
        migrations.CreateModel(
            name='ProductCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Нэр')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
            ],
            options={
                'verbose_name': 'Бүтээгдэхүүн ангилал',
                'verbose_name_plural': 'Бүтээгдэхүүн ангилалууд',
                'db_table': 'sales_product_cat',
            },
        ),
        migrations.CreateModel(
            name='SellItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('picture', models.ImageField(max_length=256, unique=True, upload_to='', verbose_name='Зураг')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Гарчиг')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='brand_items', to='sales.brandmodel', verbose_name='Brand')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cat_items', to='sales.productcategorymodel', verbose_name='Төрөл')),
            ],
            options={
                'verbose_name': 'Худалдах бараа',
                'verbose_name_plural': 'Худалдах бараанууд',
                'db_table': 'sales_items',
            },
        ),
    ]
