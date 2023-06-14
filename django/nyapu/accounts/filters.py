from django_filters import rest_framework as filters
from accounts.models import CustomUser, Relationship


class CustomUsersFilter(filters.FilterSet):
    """カスタムユーザーを文字列検索するクラス"""
    query = filters.CharFilter(field_name='query', method='user_search')

    class Meta:
        model = CustomUser
        field = ['query']

    def user_search(self, queryset, name, value):
        """カスタムユーザー検索用メソッド"""
        return queryset.filter(
            filters.Q(username__icontains=value) |
            filters.Q(profile__icontains=value)
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
