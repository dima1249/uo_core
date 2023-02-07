# Generated by Django 3.2 on 2023-02-08 02:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sales.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_alter_sellitemattributes_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.CharField(blank=True, choices=[('IndianRed', 'IndianRed'), ('LightCoral', 'LightCoral'), ('Salmon', 'Salmon'), ('DarkSalmon', 'DarkSalmon'), ('LightSalmon', 'LightSalmon'), ('Crimson', 'Crimson'), ('Red', 'Red'), ('FireBrick', 'FireBrick'), ('DarkRed', 'DarkRed'), ('Pink', 'Pink'), ('LightPink', 'LightPink'), ('HotPink', 'HotPink'), ('DeepPink', 'DeepPink'), ('MediumVioletRed', 'MediumVioletRed'), ('PaleVioletRed', 'PaleVioletRed'), ('LightSalmon', 'LightSalmon'), ('Coral', 'Coral'), ('Tomato', 'Tomato'), ('OrangeRed', 'OrangeRed'), ('DarkOrange', 'DarkOrange'), ('Orange', 'Orange'), ('Gold', 'Gold'), ('Yellow', 'Yellow'), ('LightYellow', 'LightYellow'), ('LemonChiffon', 'LemonChiffon'), ('LightGoldenrodYellow', 'LightGoldenrodYellow'), ('PapayaWhip', 'PapayaWhip'), ('Moccasin', 'Moccasin'), ('PeachPuff', 'PeachPuff'), ('PaleGoldenrod', 'PaleGoldenrod'), ('Khaki', 'Khaki'), ('DarkKhaki', 'DarkKhaki'), ('Lavender', 'Lavender'), ('Thistle', 'Thistle'), ('Plum', 'Plum'), ('Violet', 'Violet'), ('Orchid', 'Orchid'), ('Fuchsia', 'Fuchsia'), ('Magenta', 'Magenta'), ('MediumOrchid', 'MediumOrchid'), ('MediumPurple', 'MediumPurple'), ('RebeccaPurple', 'RebeccaPurple'), ('BlueViolet', 'BlueViolet'), ('DarkViolet', 'DarkViolet'), ('DarkOrchid', 'DarkOrchid'), ('DarkMagenta', 'DarkMagenta'), ('Purple', 'Purple'), ('Indigo', 'Indigo'), ('SlateBlue', 'SlateBlue'), ('DarkSlateBlue', 'DarkSlateBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('GreenYellow', 'GreenYellow'), ('Chartreuse', 'Chartreuse'), ('LawnGreen', 'LawnGreen'), ('Lime', 'Lime'), ('LimeGreen', 'LimeGreen'), ('PaleGreen', 'PaleGreen'), ('LightGreen', 'LightGreen'), ('MediumSpringGreen', 'MediumSpringGreen'), ('SpringGreen', 'SpringGreen'), ('MediumSeaGreen', 'MediumSeaGreen'), ('SeaGreen', 'SeaGreen'), ('ForestGreen', 'ForestGreen'), ('Green', 'Green'), ('DarkGreen', 'DarkGreen'), ('YellowGreen', 'YellowGreen'), ('OliveDrab', 'OliveDrab'), ('Olive', 'Olive'), ('DarkOliveGreen', 'DarkOliveGreen'), ('MediumAquamarine', 'MediumAquamarine'), ('DarkSeaGreen', 'DarkSeaGreen'), ('LightSeaGreen', 'LightSeaGreen'), ('DarkCyan', 'DarkCyan'), ('Teal', 'Teal'), ('Aqua', 'Aqua'), ('Cyan', 'Cyan'), ('LightCyan', 'LightCyan'), ('PaleTurquoise', 'PaleTurquoise'), ('Aquamarine', 'Aquamarine'), ('Turquoise', 'Turquoise'), ('MediumTurquoise', 'MediumTurquoise'), ('DarkTurquoise', 'DarkTurquoise'), ('CadetBlue', 'CadetBlue'), ('SteelBlue', 'SteelBlue'), ('LightSteelBlue', 'LightSteelBlue'), ('PowderBlue', 'PowderBlue'), ('LightBlue', 'LightBlue'), ('SkyBlue', 'SkyBlue'), ('LightSkyBlue', 'LightSkyBlue'), ('DeepSkyBlue', 'DeepSkyBlue'), ('DodgerBlue', 'DodgerBlue'), ('CornflowerBlue', 'CornflowerBlue'), ('MediumSlateBlue', 'MediumSlateBlue'), ('RoyalBlue', 'RoyalBlue'), ('Blue', 'Blue'), ('MediumBlue', 'MediumBlue'), ('DarkBlue', 'DarkBlue'), ('Navy', 'Navy'), ('MidnightBlue', 'MidnightBlue'), ('Cornsilk', 'Cornsilk'), ('BlanchedAlmond', 'BlanchedAlmond'), ('Bisque', 'Bisque'), ('NavajoWhite', 'NavajoWhite'), ('Wheat', 'Wheat'), ('BurlyWood', 'BurlyWood'), ('Tan', 'Tan'), ('RosyBrown', 'RosyBrown'), ('SandyBrown', 'SandyBrown'), ('Goldenrod', 'Goldenrod'), ('DarkGoldenrod', 'DarkGoldenrod'), ('Peru', 'Peru'), ('Chocolate', 'Chocolate'), ('SaddleBrown', 'SaddleBrown'), ('Sienna', 'Sienna'), ('Brown', 'Brown'), ('Maroon', 'Maroon'), ('White', 'White'), ('Snow', 'Snow'), ('HoneyDew', 'HoneyDew'), ('MintCream', 'MintCream'), ('Azure', 'Azure'), ('AliceBlue', 'AliceBlue'), ('GhostWhite', 'GhostWhite'), ('WhiteSmoke', 'WhiteSmoke'), ('SeaShell', 'SeaShell'), ('Beige', 'Beige'), ('OldLace', 'OldLace'), ('FloralWhite', 'FloralWhite'), ('Ivory', 'Ivory'), ('AntiqueWhite', 'AntiqueWhite'), ('Linen', 'Linen'), ('LavenderBlush', 'LavenderBlush'), ('MistyRose', 'MistyRose'), ('Gainsboro', 'Gainsboro'), ('LightGray', 'LightGray'), ('Silver', 'Silver'), ('DarkGray', 'DarkGray'), ('Gray', 'Gray'), ('DimGray', 'DimGray'), ('LightSlateGray', 'LightSlateGray'), ('SlateGray', 'SlateGray'), ('DarkSlateGray', 'DarkSlateGray'), ('Black', 'Black')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.sellitemtypemodel', verbose_name='Загвар'),
        ),
        migrations.AlterField(
            model_name='sellitemattributes',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Онцгой үнэ'),
        ),
        migrations.AlterField(
            model_name='sellitemattributes',
            name='quantity',
            field=models.IntegerField(default=1, validators=[sales.models.validate_zero], verbose_name='Бэлэн байгаа тоо (<0 захиалах хязгаар)'),
        ),
    ]
