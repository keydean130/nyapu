# Generated by Django 4.0.2 on 2022-07-30 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0011_alter_diary_lat_alter_diary_lon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='本文')),
                ('commented_at', models.DateTimeField(auto_now_add=True, verbose_name='コメント日時')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('diary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.diary')),
            ],
        ),
    ]
