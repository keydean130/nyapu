from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='images', verbose_name='プロフィール画像', blank=True, null=True)
    profile = models.TextField(verbose_name='自己紹介', max_length=420, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'CustomUser'


class Relationship(models.Model):

    # 自分をフォローしてくれている人
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    # 自分がフォローしている人
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)

    # 重複してフォロー関係を作成しないように制約を設定する
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'],
                                    name='user-relationship')
        ]

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)
