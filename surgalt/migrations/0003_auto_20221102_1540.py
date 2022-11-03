# Generated by Django 3.2 on 2022-11-02 15:40

from django.db import migrations, models
import uo_core.utills


class Migration(migrations.Migration):

    dependencies = [
        ('surgalt', '0002_auto_20221026_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachermodel',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=uo_core.utills.PathAndRename('teacher_pics/'), verbose_name='Зураг'),
        ),
        migrations.AddField(
            model_name='teachermodel',
            name='social',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Сошиал линк'),
        ),
    ]