# Generated by Django 3.2.14 on 2022-10-12 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0019_auto_20221012_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='photo1',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='写真１'),
        ),
    ]