from django_filters import rest_framework as filters
from accounts.models import CustomUser, Relationship
import numpy as np


class FollowersFilter(filters.FilterSet):
    """ログインユーザーをフォローしているユーザーをフィルタ―するクラス"""

    followers = filters.NumberFilter(field_name='following_id', lookup_expr='exact')

    class Meta:
        model = Relationship
        fields = ['followers']


class FollowingsFilter(filters.FilterSet):
    """ログインユーザーがフォローしているユーザーをフィルタ―するクラス"""

    followings = filters.NumberFilter(field_name='follower_id', lookup_expr='exact')

    class Meta:
        model = Relationship
        fields = ['followings']
