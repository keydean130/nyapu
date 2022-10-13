from lib2to3.pgen2.pgen import PgenGrammar
from django.db import models


class Diary(models.Model):
    '''日記モデル'''
    user = models.ForeignKey('accounts.CustomUser', verbose_name='ユーザー', related_name='user', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=2200, blank=True, null=True)
    content = models.TextField(verbose_name='本文', max_length=2200, blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真１', blank=True, null=True, default='static/assets/img/nyapu.png')
    photo2 = models.ImageField(verbose_name='写真２', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真３', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lat = models.DecimalField(verbose_name="緯度", max_digits=9, decimal_places=6, default=35.709)
    lon = models.DecimalField(verbose_name="経度", max_digits=9, decimal_places=6, default=139.7319)

    class Meta:
        verbose_name_plural = 'Diary'

    def __str__(self):
        return str(self.title)


class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    like_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name='いいねした日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Like'

    def __str__(self):
        return "{} : {}".format(self.diary.title, self.like_user.username)


class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    comment_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='コメント', blank=False, null=False)
    commented_at = models.DateTimeField(verbose_name='コメント日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comment'

    def __str__(self):
        return str(self.text[:112])
