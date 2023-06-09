# Generated by Django 3.2.16 on 2022-10-12 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0017_alter_diary_photo1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, default=35.709, max_digits=9, null=True, verbose_name='緯度'),
        ),
        migrations.AlterField(
            model_name='diary',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=6, default=139.7319, max_digits=9, null=True, verbose_name='経度'),
        ),
        migrations.AlterField(
            model_name='diary',
            name='photo1',
            field=models.ImageField(upload_to='', verbose_name='写真１'),
        ),
    ]