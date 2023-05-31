# Generated by Django 3.2 on 2023-05-31 13:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sales.models.models
import simple_history.models
import uo_core.utills


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=250)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('primary', models.BooleanField(default=False)),
                ('building_number', models.IntegerField(blank=True, null=True)),
                ('apartment_number', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
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
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сагс',
                'verbose_name_plural': 'Сагснууд',
                'db_table': 'sales_carts',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('order_number', models.CharField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(blank=True, max_length=250, null=True)),
                ('delivery', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('p', 'Pending'), ('o', 'Completed'), ('c', 'Canceled')], default='p', max_length=1)),
                ('is_paid', models.BooleanField(default=False)),
                ('to_paid', models.FloatField(default=0, verbose_name='Төлөгдсөн дүн')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_address', to='sales.address')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Захиалга',
                'verbose_name_plural': '02 Захиалганууд',
                'db_table': 'sales_orders',
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
                ('picture', models.ImageField(blank=True, null=True, upload_to=uo_core.utills.PathAndRename('product_categories/'), verbose_name='Зураг')),
            ],
            options={
                'verbose_name': 'Бүтээгдэхүүн ангилал',
                'verbose_name_plural': 'Бүтээгдэхүүн ангилалууд',
                'db_table': 'sales_product_cat',
            },
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('ref_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='ref number')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment id')),
                ('transaction_type', models.IntegerField(blank=True, choices=[(1, 'ОРЛОГО'), (2, 'ЗАРЛАГА')], null=True, verbose_name='Гүйлгээний төрөл')),
                ('payment_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Гүйлгээний утга')),
                ('amount', models.FloatField(blank=True, default=0, null=True, verbose_name='Үнэ')),
                ('currency', models.CharField(blank=True, default='MNT', max_length=10, null=True, verbose_name='Мөнгөн тэмдэгт')),
                ('account_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='Данс эзэмшигчийн ҮА чиглэл')),
                ('is_refunded', models.BooleanField(blank=True, default=0, null=True, verbose_name='Төлбөр буцаасан')),
                ('is_hand_charge', models.BooleanField(blank=True, default=0, null=True, verbose_name='Гараар нэмсэн')),
                ('charge_payment_called', models.IntegerField(blank=True, default=0, null=True, verbose_name='charged count')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_transaction_user', to=settings.AUTH_USER_MODEL, verbose_name='Үүсгэсэн хэрэглэгч')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deleted_transaction_user', to=settings.AUTH_USER_MODEL, verbose_name='Устгасан хэрэглэгч')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_transaction_user', to=settings.AUTH_USER_MODEL, verbose_name='Шинэчилсэн хэрэглэгч')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'gok_transaction',
            },
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
                'verbose_name': 'Бүтээгдэхүүн Загвар',
                'verbose_name_plural': 'Бүтээгдэхүүн Загварууд',
                'db_table': 'sales_product_type',
            },
        ),
        migrations.CreateModel(
            name='SellItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Гарчиг')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('price', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Үнэ (min)')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brand_items', to='sales.brandmodel', verbose_name='Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat_items', to='sales.productcategorymodel', verbose_name='Төрөл')),
            ],
            options={
                'verbose_name': 'Худалдах бараа',
                'verbose_name_plural': '01 Худалдах бараанууд',
                'db_table': 'sales_items',
            },
        ),
        migrations.CreateModel(
            name='QpayInvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('ref_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='ref number')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment id')),
                ('qpay_qr_code', models.TextField(blank=True, null=True, verbose_name='QPAY QR code')),
                ('qpay_short_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='QPAY short ulr')),
                ('amount', models.FloatField(blank=True, default=0, null=True, verbose_name='мөнгөн дүн')),
                ('currency', models.CharField(blank=True, default='MNT', max_length=10, null=True, verbose_name='Мөнгөн тэмдэгт')),
                ('invoice_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='invoice name')),
                ('phone_number', models.CharField(blank=True, max_length=150, null=True, verbose_name='phone')),
                ('invoice_description', models.CharField(blank=True, max_length=200, null=True, verbose_name='invoice discription')),
                ('qr_image', models.TextField(blank=True, null=True, verbose_name='qr image')),
                ('deep_link', models.TextField(blank=True, null=True, verbose_name='deeplinks')),
                ('is_paid', models.BooleanField(blank=True, default=False, null=True, verbose_name='Төлөгдсөн')),
                ('is_company', models.BooleanField(blank=True, default=False, null=True, verbose_name='Байгууллагаар')),
                ('company_register', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Байгууллагын регистер')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_qpay_user', to=settings.AUTH_USER_MODEL, verbose_name='Үүсгэсэн хэрэглэгч')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deleted_qpay_user', to=settings.AUTH_USER_MODEL, verbose_name='Устгасан хэрэглэгч')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_qpay_user', to=settings.AUTH_USER_MODEL, verbose_name='Шинэчилсэн хэрэглэгч')),
            ],
            options={
                'verbose_name': 'Qpay invoice',
                'verbose_name_plural': 'Qpay invoices',
                'db_table': 'sales_qpay_invoice',
            },
        ),
        migrations.CreateModel(
            name='ProductImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Picture', max_length=100, null=True, verbose_name='Зураг гарчиг')),
                ('picture', models.ImageField(upload_to=uo_core.utills.PathAndRename('product_pics/'), verbose_name='Зураг')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='эрэмбэ')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='image_product', to='sales.sellitemmodel', verbose_name='Зурагнууд')),
            ],
            options={
                'verbose_name': 'Худалдах барааны зурагнууд',
                'db_table': 'sales_item_picture',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('quantity', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='sales.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='sales.sellitemmodel')),
            ],
            options={
                'verbose_name': 'Захиалганд харгалзах бараа',
                'verbose_name_plural': 'Захиалганд харгалзах бараанууд',
                'db_table': 'sales_order_items',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTransactionModel',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('ref_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='ref number')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment id')),
                ('transaction_type', models.IntegerField(blank=True, choices=[(1, 'ОРЛОГО'), (2, 'ЗАРЛАГА')], null=True, verbose_name='Гүйлгээний төрөл')),
                ('payment_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Гүйлгээний утга')),
                ('amount', models.FloatField(blank=True, default=0, null=True, verbose_name='Үнэ')),
                ('currency', models.CharField(blank=True, default='MNT', max_length=10, null=True, verbose_name='Мөнгөн тэмдэгт')),
                ('account_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='Данс эзэмшигчийн ҮА чиглэл')),
                ('is_refunded', models.BooleanField(blank=True, default=0, null=True, verbose_name='Төлбөр буцаасан')),
                ('is_hand_charge', models.BooleanField(blank=True, default=0, null=True, verbose_name='Гараар нэмсэн')),
                ('charge_payment_called', models.IntegerField(blank=True, default=0, null=True, verbose_name='charged count')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Үүсгэсэн хэрэглэгч')),
                ('deleted_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Устгасан хэрэглэгч')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Шинэчилсэн хэрэглэгч')),
            ],
            options={
                'verbose_name': 'historical Transaction',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('order_number', models.CharField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(blank=True, max_length=250, null=True)),
                ('delivery', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('p', 'Pending'), ('o', 'Completed'), ('c', 'Canceled')], default='p', max_length=1)),
                ('is_paid', models.BooleanField(default=False)),
                ('to_paid', models.FloatField(default=0, verbose_name='Төлөгдсөн дүн')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('address', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sales.address')),
                ('buyer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Захиалга',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('in_store', models.BooleanField(default=True)),
                ('size', models.CharField(blank=True, max_length=5, null=True)),
                ('color', models.CharField(blank=True, choices=[('IndianRed', 'IndianRed'), ('LightCoral', 'LightCoral'), ('Salmon', 'Salmon'), ('DarkSalmon', 'DarkSalmon'), ('LightSalmon', 'LightSalmon'), ('Crimson', 'Crimson'), ('Red', 'Red'), ('FireBrick', 'FireBrick'), ('DarkRed', 'DarkRed'), ('Pink', 'Pink'), ('LightPink', 'LightPink'), ('HotPink', 'HotPink'), ('DeepPink', 'DeepPink'), ('MediumVioletRed', 'MediumVioletRed'), ('PaleVioletRed', 'PaleVioletRed'), ('LightSalmon', 'LightSalmon'), ('Coral', 'Coral'), ('Tomato', 'Tomato'), ('OrangeRed', 'OrangeRed'), ('DarkOrange', 'DarkOrange'), ('Orange', 'Orange'), ('Gold', 'Gold'), ('Yellow', 'Yellow'), ('LightYellow', 'LightYellow'), ('LemonChiffon', 'LemonChiffon'), ('LightGoldenrodYellow', 'LightGoldenrodYellow'), ('PapayaWhip', 'PapayaWhip'), ('Moccasin', 'Moccasin'), ('PeachPuff', 'PeachPuff'), ('PaleGoldenrod', 'PaleGoldenrod'), ('Khaki', 'Khaki'), ('DarkKhaki', 'DarkKhaki'), ('Lavender', 'Lavender'), ('Thistle', 'Thistle'), ('Plum', 'Plum'), ('Violet', 'Violet'), ('Orchid', 'Orchid'), ('Fuchsia', 'Fuchsia'), ('Magenta', 'Magenta'), ('MediumOrchid', 'MediumOrchid'), ('MediumPurple', 'MediumPurple'), ('RebeccaPurple', 'RebeccaPurple'), ('BlueViolet', 'BlueViolet'), ('DarkViolet', 'DarkViolet'), ('DarkOrchid', 'DarkOrchid'), ('DarkMagenta', 'DarkMagenta'), ('Purple', 'Purple'), ('Indigo', 'Indigo'), ('SlateBlue', 'SlateBlue'), ('DarkSlateBlue', 'DarkSlateBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('GreenYellow', 'GreenYellow'), ('Chartreuse', 'Chartreuse'), ('LawnGreen', 'LawnGreen'), ('Lime', 'Lime'), ('LimeGreen', 'LimeGreen'), ('PaleGreen', 'PaleGreen'), ('LightGreen', 'LightGreen'), ('MediumSpringGreen', 'MediumSpringGreen'), ('SpringGreen', 'SpringGreen'), ('MediumSeaGreen', 'MediumSeaGreen'), ('SeaGreen', 'SeaGreen'), ('ForestGreen', 'ForestGreen'), ('Green', 'Green'), ('DarkGreen', 'DarkGreen'), ('YellowGreen', 'YellowGreen'), ('OliveDrab', 'OliveDrab'), ('Olive', 'Olive'), ('DarkOliveGreen', 'DarkOliveGreen'), ('MediumAquamarine', 'MediumAquamarine'), ('DarkSeaGreen', 'DarkSeaGreen'), ('LightSeaGreen', 'LightSeaGreen'), ('DarkCyan', 'DarkCyan'), ('Teal', 'Teal'), ('Aqua', 'Aqua'), ('Cyan', 'Cyan'), ('LightCyan', 'LightCyan'), ('PaleTurquoise', 'PaleTurquoise'), ('Aquamarine', 'Aquamarine'), ('Turquoise', 'Turquoise'), ('MediumTurquoise', 'MediumTurquoise'), ('DarkTurquoise', 'DarkTurquoise'), ('CadetBlue', 'CadetBlue'), ('SteelBlue', 'SteelBlue'), ('LightSteelBlue', 'LightSteelBlue'), ('PowderBlue', 'PowderBlue'), ('LightBlue', 'LightBlue'), ('SkyBlue', 'SkyBlue'), ('LightSkyBlue', 'LightSkyBlue'), ('DeepSkyBlue', 'DeepSkyBlue'), ('DodgerBlue', 'DodgerBlue'), ('CornflowerBlue', 'CornflowerBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('RoyalBlue', 'RoyalBlue'), ('Blue', 'Blue'), ('MediumBlue', 'MediumBlue'), ('DarkBlue', 'DarkBlue'), ('Navy', 'Navy'), ('MidnightBlue', 'MidnightBlue'), ('Cornsilk', 'Cornsilk'), ('BlanchedAlmond', 'BlanchedAlmond'), ('Bisque', 'Bisque'), ('NavajoWhite', 'NavajoWhite'), ('Wheat', 'Wheat'), ('BurlyWood', 'BurlyWood'), ('Tan', 'Tan'), ('RosyBrown', 'RosyBrown'), ('SandyBrown', 'SandyBrown'), ('Goldenrod', 'Goldenrod'), ('DarkGoldenrod', 'DarkGoldenrod'), ('Peru', 'Peru'), ('Chocolate', 'Chocolate'), ('SaddleBrown', 'SaddleBrown'), ('Sienna', 'Sienna'), ('Brown', 'Brown'), ('Maroon', 'Maroon'), ('White', 'White'), ('Snow', 'Snow'), ('HoneyDew', 'HoneyDew'), ('MintCream', 'MintCream'), ('Azure', 'Azure'), ('AliceBlue', 'AliceBlue'), ('GhostWhite', 'GhostWhite'), ('WhiteSmoke', 'WhiteSmoke'), ('SeaShell', 'SeaShell'), ('Beige', 'Beige'), ('OldLace', 'OldLace'), ('FloralWhite', 'FloralWhite'), ('Ivory', 'Ivory'), ('AntiqueWhite', 'AntiqueWhite'), ('Linen', 'Linen'), ('LavenderBlush', 'LavenderBlush'), ('MistyRose', 'MistyRose'), ('Gainsboro', 'Gainsboro'), ('LightGray', 'LightGray'), ('Silver', 'Silver'), ('DarkGray', 'DarkGray'), ('Gray', 'Gray'), ('DimGray', 'DimGray'), ('LightSlateGray', 'LightSlateGray'), ('SlateGray', 'SlateGray'), ('DarkSlateGray', 'DarkSlateGray'), ('Black', 'Black')], max_length=20, null=True)),
                ('color_code', models.CharField(blank=True, choices=[('IndianRed', 'IndianRed'), ('LightCoral', 'LightCoral'), ('Salmon', 'Salmon'), ('DarkSalmon', 'DarkSalmon'), ('LightSalmon', 'LightSalmon'), ('Crimson', 'Crimson'), ('Red', 'Red'), ('FireBrick', 'FireBrick'), ('DarkRed', 'DarkRed'), ('Pink', 'Pink'), ('LightPink', 'LightPink'), ('HotPink', 'HotPink'), ('DeepPink', 'DeepPink'), ('MediumVioletRed', 'MediumVioletRed'), ('PaleVioletRed', 'PaleVioletRed'), ('LightSalmon', 'LightSalmon'), ('Coral', 'Coral'), ('Tomato', 'Tomato'), ('OrangeRed', 'OrangeRed'), ('DarkOrange', 'DarkOrange'), ('Orange', 'Orange'), ('Gold', 'Gold'), ('Yellow', 'Yellow'), ('LightYellow', 'LightYellow'), ('LemonChiffon', 'LemonChiffon'), ('LightGoldenrodYellow', 'LightGoldenrodYellow'), ('PapayaWhip', 'PapayaWhip'), ('Moccasin', 'Moccasin'), ('PeachPuff', 'PeachPuff'), ('PaleGoldenrod', 'PaleGoldenrod'), ('Khaki', 'Khaki'), ('DarkKhaki', 'DarkKhaki'), ('Lavender', 'Lavender'), ('Thistle', 'Thistle'), ('Plum', 'Plum'), ('Violet', 'Violet'), ('Orchid', 'Orchid'), ('Fuchsia', 'Fuchsia'), ('Magenta', 'Magenta'), ('MediumOrchid', 'MediumOrchid'), ('MediumPurple', 'MediumPurple'), ('RebeccaPurple', 'RebeccaPurple'), ('BlueViolet', 'BlueViolet'), ('DarkViolet', 'DarkViolet'), ('DarkOrchid', 'DarkOrchid'), ('DarkMagenta', 'DarkMagenta'), ('Purple', 'Purple'), ('Indigo', 'Indigo'), ('SlateBlue', 'SlateBlue'), ('DarkSlateBlue', 'DarkSlateBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('GreenYellow', 'GreenYellow'), ('Chartreuse', 'Chartreuse'), ('LawnGreen', 'LawnGreen'), ('Lime', 'Lime'), ('LimeGreen', 'LimeGreen'), ('PaleGreen', 'PaleGreen'), ('LightGreen', 'LightGreen'), ('MediumSpringGreen', 'MediumSpringGreen'), ('SpringGreen', 'SpringGreen'), ('MediumSeaGreen', 'MediumSeaGreen'), ('SeaGreen', 'SeaGreen'), ('ForestGreen', 'ForestGreen'), ('Green', 'Green'), ('DarkGreen', 'DarkGreen'), ('YellowGreen', 'YellowGreen'), ('OliveDrab', 'OliveDrab'), ('Olive', 'Olive'), ('DarkOliveGreen', 'DarkOliveGreen'), ('MediumAquamarine', 'MediumAquamarine'), ('DarkSeaGreen', 'DarkSeaGreen'), ('LightSeaGreen', 'LightSeaGreen'), ('DarkCyan', 'DarkCyan'), ('Teal', 'Teal'), ('Aqua', 'Aqua'), ('Cyan', 'Cyan'), ('LightCyan', 'LightCyan'), ('PaleTurquoise', 'PaleTurquoise'), ('Aquamarine', 'Aquamarine'), ('Turquoise', 'Turquoise'), ('MediumTurquoise', 'MediumTurquoise'), ('DarkTurquoise', 'DarkTurquoise'), ('CadetBlue', 'CadetBlue'), ('SteelBlue', 'SteelBlue'), ('LightSteelBlue', 'LightSteelBlue'), ('PowderBlue', 'PowderBlue'), ('LightBlue', 'LightBlue'), ('SkyBlue', 'SkyBlue'), ('LightSkyBlue', 'LightSkyBlue'), ('DeepSkyBlue', 'DeepSkyBlue'), ('DodgerBlue', 'DodgerBlue'), ('CornflowerBlue', 'CornflowerBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('RoyalBlue', 'RoyalBlue'), ('Blue', 'Blue'), ('MediumBlue', 'MediumBlue'), ('DarkBlue', 'DarkBlue'), ('Navy', 'Navy'), ('MidnightBlue', 'MidnightBlue'), ('Cornsilk', 'Cornsilk'), ('BlanchedAlmond', 'BlanchedAlmond'), ('Bisque', 'Bisque'), ('NavajoWhite', 'NavajoWhite'), ('Wheat', 'Wheat'), ('BurlyWood', 'BurlyWood'), ('Tan', 'Tan'), ('RosyBrown', 'RosyBrown'), ('SandyBrown', 'SandyBrown'), ('Goldenrod', 'Goldenrod'), ('DarkGoldenrod', 'DarkGoldenrod'), ('Peru', 'Peru'), ('Chocolate', 'Chocolate'), ('SaddleBrown', 'SaddleBrown'), ('Sienna', 'Sienna'), ('Brown', 'Brown'), ('Maroon', 'Maroon'), ('White', 'White'), ('Snow', 'Snow'), ('HoneyDew', 'HoneyDew'), ('MintCream', 'MintCream'), ('Azure', 'Azure'), ('AliceBlue', 'AliceBlue'), ('GhostWhite', 'GhostWhite'), ('WhiteSmoke', 'WhiteSmoke'), ('SeaShell', 'SeaShell'), ('Beige', 'Beige'), ('OldLace', 'OldLace'), ('FloralWhite', 'FloralWhite'), ('Ivory', 'Ivory'), ('AntiqueWhite', 'AntiqueWhite'), ('Linen', 'Linen'), ('LavenderBlush', 'LavenderBlush'), ('MistyRose', 'MistyRose'), ('Gainsboro', 'Gainsboro'), ('LightGray', 'LightGray'), ('Silver', 'Silver'), ('DarkGray', 'DarkGray'), ('Gray', 'Gray'), ('DimGray', 'DimGray'), ('LightSlateGray', 'LightSlateGray'), ('SlateGray', 'SlateGray'), ('DarkSlateGray', 'DarkSlateGray'), ('Black', 'Black')], max_length=20, null=True)),
                ('price', models.FloatField(default=0, verbose_name='Ширхэг үнэ')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='sales.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_product', to='sales.sellitemmodel')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.sellitemtypemodel', verbose_name='Загвар')),
            ],
            options={
                'verbose_name': 'Сагсан дахь бараа',
                'verbose_name_plural': 'Сагсан дахь бараанууд',
                'db_table': 'sales_cart_item',
            },
        ),
        migrations.CreateModel(
            name='SellItemAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.FloatField(blank=True, null=True)),
                ('size_unit', models.CharField(choices=[('UNIT', 'UNIT'), ('S', 'S'), ('L', 'L'), ('M', 'M'), ('XL', 'XL'), ('XXL', 'XXL'), ('Q', 'Q'), ('ST', 'ST')], default='UNIT', max_length=20)),
                ('color', models.CharField(blank=True, choices=[('IndianRed', 'IndianRed'), ('LightCoral', 'LightCoral'), ('Salmon', 'Salmon'), ('DarkSalmon', 'DarkSalmon'), ('LightSalmon', 'LightSalmon'), ('Crimson', 'Crimson'), ('Red', 'Red'), ('FireBrick', 'FireBrick'), ('DarkRed', 'DarkRed'), ('Pink', 'Pink'), ('LightPink', 'LightPink'), ('HotPink', 'HotPink'), ('DeepPink', 'DeepPink'), ('MediumVioletRed', 'MediumVioletRed'), ('PaleVioletRed', 'PaleVioletRed'), ('LightSalmon', 'LightSalmon'), ('Coral', 'Coral'), ('Tomato', 'Tomato'), ('OrangeRed', 'OrangeRed'), ('DarkOrange', 'DarkOrange'), ('Orange', 'Orange'), ('Gold', 'Gold'), ('Yellow', 'Yellow'), ('LightYellow', 'LightYellow'), ('LemonChiffon', 'LemonChiffon'), ('LightGoldenrodYellow', 'LightGoldenrodYellow'), ('PapayaWhip', 'PapayaWhip'), ('Moccasin', 'Moccasin'), ('PeachPuff', 'PeachPuff'), ('PaleGoldenrod', 'PaleGoldenrod'), ('Khaki', 'Khaki'), ('DarkKhaki', 'DarkKhaki'), ('Lavender', 'Lavender'), ('Thistle', 'Thistle'), ('Plum', 'Plum'), ('Violet', 'Violet'), ('Orchid', 'Orchid'), ('Fuchsia', 'Fuchsia'), ('Magenta', 'Magenta'), ('MediumOrchid', 'MediumOrchid'), ('MediumPurple', 'MediumPurple'), ('RebeccaPurple', 'RebeccaPurple'), ('BlueViolet', 'BlueViolet'), ('DarkViolet', 'DarkViolet'), ('DarkOrchid', 'DarkOrchid'), ('DarkMagenta', 'DarkMagenta'), ('Purple', 'Purple'), ('Indigo', 'Indigo'), ('SlateBlue', 'SlateBlue'), ('DarkSlateBlue', 'DarkSlateBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('GreenYellow', 'GreenYellow'), ('Chartreuse', 'Chartreuse'), ('LawnGreen', 'LawnGreen'), ('Lime', 'Lime'), ('LimeGreen', 'LimeGreen'), ('PaleGreen', 'PaleGreen'), ('LightGreen', 'LightGreen'), ('MediumSpringGreen', 'MediumSpringGreen'), ('SpringGreen', 'SpringGreen'), ('MediumSeaGreen', 'MediumSeaGreen'), ('SeaGreen', 'SeaGreen'), ('ForestGreen', 'ForestGreen'), ('Green', 'Green'), ('DarkGreen', 'DarkGreen'), ('YellowGreen', 'YellowGreen'), ('OliveDrab', 'OliveDrab'), ('Olive', 'Olive'), ('DarkOliveGreen', 'DarkOliveGreen'), ('MediumAquamarine', 'MediumAquamarine'), ('DarkSeaGreen', 'DarkSeaGreen'), ('LightSeaGreen', 'LightSeaGreen'), ('DarkCyan', 'DarkCyan'), ('Teal', 'Teal'), ('Aqua', 'Aqua'), ('Cyan', 'Cyan'), ('LightCyan', 'LightCyan'), ('PaleTurquoise', 'PaleTurquoise'), ('Aquamarine', 'Aquamarine'), ('Turquoise', 'Turquoise'), ('MediumTurquoise', 'MediumTurquoise'), ('DarkTurquoise', 'DarkTurquoise'), ('CadetBlue', 'CadetBlue'), ('SteelBlue', 'SteelBlue'), ('LightSteelBlue', 'LightSteelBlue'), ('PowderBlue', 'PowderBlue'), ('LightBlue', 'LightBlue'), ('SkyBlue', 'SkyBlue'), ('LightSkyBlue', 'LightSkyBlue'), ('DeepSkyBlue', 'DeepSkyBlue'), ('DodgerBlue', 'DodgerBlue'), ('CornflowerBlue', 'CornflowerBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('RoyalBlue', 'RoyalBlue'), ('Blue', 'Blue'), ('MediumBlue', 'MediumBlue'), ('DarkBlue', 'DarkBlue'), ('Navy', 'Navy'), ('MidnightBlue', 'MidnightBlue'), ('Cornsilk', 'Cornsilk'), ('BlanchedAlmond', 'BlanchedAlmond'), ('Bisque', 'Bisque'), ('NavajoWhite', 'NavajoWhite'), ('Wheat', 'Wheat'), ('BurlyWood', 'BurlyWood'), ('Tan', 'Tan'), ('RosyBrown', 'RosyBrown'), ('SandyBrown', 'SandyBrown'), ('Goldenrod', 'Goldenrod'), ('DarkGoldenrod', 'DarkGoldenrod'), ('Peru', 'Peru'), ('Chocolate', 'Chocolate'), ('SaddleBrown', 'SaddleBrown'), ('Sienna', 'Sienna'), ('Brown', 'Brown'), ('Maroon', 'Maroon'), ('White', 'White'), ('Snow', 'Snow'), ('HoneyDew', 'HoneyDew'), ('MintCream', 'MintCream'), ('Azure', 'Azure'), ('AliceBlue', 'AliceBlue'), ('GhostWhite', 'GhostWhite'), ('WhiteSmoke', 'WhiteSmoke'), ('SeaShell', 'SeaShell'), ('Beige', 'Beige'), ('OldLace', 'OldLace'), ('FloralWhite', 'FloralWhite'), ('Ivory', 'Ivory'), ('AntiqueWhite', 'AntiqueWhite'), ('Linen', 'Linen'), ('LavenderBlush', 'LavenderBlush'), ('MistyRose', 'MistyRose'), ('Gainsboro', 'Gainsboro'), ('LightGray', 'LightGray'), ('Silver', 'Silver'), ('DarkGray', 'DarkGray'), ('Gray', 'Gray'), ('DimGray', 'DimGray'), ('LightSlateGray', 'LightSlateGray'), ('SlateGray', 'SlateGray'), ('DarkSlateGray', 'DarkSlateGray'), ('Black', 'Black')], max_length=20, null=True)),
                ('color_code', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.IntegerField(default=1, validators=[sales.models.validate_zero], verbose_name='Бэлэн байгаа тоо (<0 захиалах хязгаар)')),
                ('price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Онцгой үнэ')),
                ('discount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Хөнгөлөлт [%]')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attributes', to='sales.sellitemmodel', verbose_name='Бүтээгдэхүүн')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.sellitemtypemodel', verbose_name='Загвар')),
            ],
            options={
                'verbose_name': 'Бараанд харгалзах тоо ширхэг',
                'verbose_name_plural': 'Бараанд харгалзах тоо ширхэг',
                'db_table': 'sales_item_attributes',
                'unique_together': {('type', 'size', 'color', 'quantity', 'price')},
            },
        ),
    ]
