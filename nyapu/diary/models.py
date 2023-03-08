from django.db import models


class Diary(models.Model):
    user = models.ForeignKey('accounts.CustomUser', verbose_name='ユーザー', related_name='user',
                             on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=30, blank=True, null=True)
    content = models.TextField(verbose_name='本文', max_length=2200, blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真１', blank=False, null=False)
    photo2 = models.ImageField(verbose_name='写真２', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真３', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True, null=True)
    lat = models.DecimalField(verbose_name='緯度', max_digits=9, decimal_places=6, default=35.709)
    lon = models.DecimalField(verbose_name='経度', max_digits=9, decimal_places=6, default=139.7319)
    photo1_most_similar_breed = models.CharField(verbose_name='写真１で最も類似した品種',
                                                 max_length=100, blank=True, null=True)
    photo1_second_similar_breed = models.CharField(verbose_name='写真１で２番目に類似した品種',
                                                   max_length=100, blank=True, null=True,)
    photo1_third_similar_breed = models.CharField(verbose_name='写真１で３番目に類似した品種',
                                                  max_length=100, blank=True, null=True,)
    photo1_most_similar_rate = models.IntegerField(verbose_name='写真１で最も高い類似率',
                                                   blank=True, null=True, default=0)
    photo1_second_similar_rate = models.IntegerField(verbose_name='写真１で2番目に高い類似率',
                                                     blank=True, null=True, default=0)
    photo1_third_similar_rate = models.IntegerField(verbose_name='写真１で3番目に高い類似率',
                                                    blank=True, null=True, default=0)

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
        return "{} : {}".format(self.diary, self.like_user)


class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    comment_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='コメント', blank=False, null=False)
    commented_at = models.DateTimeField(verbose_name='コメント日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comment'

    def __str__(self):
        return str(self.text[:112])
