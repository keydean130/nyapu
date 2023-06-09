# Generated by Django 4.0.2 on 2022-06-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('diary', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='like_diary',
            field=models.ManyToManyField(blank=True, to='diary.Diary', verbose_name='Likeした日記'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='relationship',
            constraint=models.UniqueConstraint(fields=('follower', 'following'), name='user-relationship'),
        ),
    ]