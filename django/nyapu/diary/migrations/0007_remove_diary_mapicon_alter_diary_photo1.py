# Generated by Django 4.0.2 on 2022-07-09 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0006_alter_diary_mapicon_alter_diary_photo1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diary',
            name='mapicon',
        ),
        migrations.AlterField(
            model_name='diary',
            name='photo1',
            field=models.ImageField(upload_to='', verbose_name='写真１'),
        ),
    ]