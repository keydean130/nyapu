from accounts.models import CustomUser, Relationship
from django_filters import rest_framework as filters

from django.db.models import Q


class CustomUsersFilter(filters.FilterSet):
    """カスタムユーザーを文字列検索するクラス"""
    query = filters.CharFilter(method='user_search')

    class Meta:
        model = CustomUser
        fields = ['query']

    def user_search(self, queryset, name, value):
        """カスタムユーザー検索用メソッド"""
        return queryset.filter(
            Q(username__icontains=value) |
            Q(profile__icontains=value)
        )


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
