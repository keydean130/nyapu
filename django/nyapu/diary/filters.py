from django_filters import rest_framework as filters
from diary.models import Diary, Like
import numpy as np


class DiariesFilter(filters.FilterSet):
    """日記を文字列検索するクラス"""

    query = filters.CharFilter(field_name='query', method='user_search')

    class Meta:
        model = Diary
        field = ['query']

    def user_search(self, queryset, name, value):
        """日記検索用メソッド"""
        return queryset.filter(
            filters.Q(title__icontains=value) |
            filters.Q(content__icontains=value)
        )


class MyDiariesFilter(filters.FilterSet):
    """ログインユーザーが投稿した日記をフィルタ―するクラス"""

    profile = filters.NumberFilter(field_name='user_id', lookup_expr='exact')

    class Meta:
        model = Diary
        fields = ['profile']


class LikedDiariesFilter(filters.FilterSet):
    """ログインユーザーがいいねした日記をフィルタ―するクラス"""

    liked_diaries = filters.NumberFilter(field_name='user_id', method='get_queryset')

    class Meta:
        model = Diary
        fields = ['liked_diaries']

    def get_queryset(self, queryset, name, value):
        # Like済みの日記のidをliked_diariesとして取得
        liked_diary_id_list = (Like.objects.filter(like_user__id=value)).values_list('diary_id')
        # Like済みの日記があれば
        if liked_diary_id_list:
            # Like済みの日記のオブジェクトをlike_diary_listに格納
            queryset = queryset.filter(id__in=liked_diary_id_list)
        else :
            queryset = None
        return queryset


class RecentDiariesFilter(filters.FilterSet):
    """おすすめの日記をフィルタ―するクラス"""

    recent_diaries = filters.NumberFilter(field_name='user_id', method='get_queryset')

    class Meta:
        model = Diary
        fields = ['recent_diaries']

    def get_queryset(self, queryset, name, value):
        # ユーザーが直近で更新した日記のオブジェクトを取得
        latest_diary = queryset.filter(user__id=value).order_by('-updated_at').first()
        # 投稿した日記がなければ
        if not latest_diary:
            return None
        # ユーザが直近で更新した日記の猫の品種を取得
        cat_breed = recent_diary.photo1_most_similar_breed
        # ユーザが直近で更新した日記の猫の品種と同じ、他のユーザが直近で更新した日記があれば
        if queryset.filter(photo1_most_similar_breed=cat_breed).exclude(user__id=value):
            # ユーザが直近で更新した日記の猫の品種と同じ、他のユーザが直近で更新した日記を取得
            queryset = queryset.filter(photo1_most_similar_breed=cat_breed).exclude(
                user__id=value).order_by('-updated_at').first()
        else:
            queryset = None
        return queryset


class NearestDiariesFilter(filters.FilterSet):
    """近所の日記をフィルタ―するクラス"""

    nearest_diaries = filters.NumberFilter(field_name='user_id',  method='get_queryset')

    class Meta:
        model = Diary
        fields = ['nearest_diaries']

    def get_queryset(self, queryset, name, value):
        # ユーザーが直近で更新した日記のオブジェクトを取得
        latest_diary = queryset.filter(user__id=value).order_by('-updated_at').first()
        # 投稿した日記がなければ
        if not latest_diary:
            return None
        # 他のユーザが直近で更新した日記、最大100件を取得
        other_user_recent_updated_diaries = queryset.exclude(
            user__id=value).order_by('-updated_at')[0:99]
        # 他のユーザが直近で更新した日記がなければ
        if not other_user_recent_updated_diaries:
            return None
        # ユーザが直近で更新した日記の、最寄りの日記を取得
        nearest_diary = self.nearest_diary(recent_diary, other_user_recent_updated_diaries)
        # ユーザが直近で更新した日記の、最寄りの日記がなければ
        if not nearest_diary:
            return None
        queryset = queryset.filter(id=nearest_diary.id)
        return queryset

    def nearest_diary(self, diary, diaries):
        # diaryの位置情報の配列作成
        recent_geo = [diary.lat, diary.lon]
        # diariesの位置情報の配列作成
        lat_idx = []
        lon_idx = []
        # クエリ―セットでオブジェクトの指定要素のみを取得
        for d_lat, d_lon in zip(diaries.values_list('lat'),
                                diaries.values_list('lon')):
            # タプルから要素を取り出して配列に格納
            lat_idx.append(d_lat[0])
            lon_idx.append(d_lon[0])
        # 位置情報の配列を設定
        geo_idx = [lat_idx, lon_idx]
        # 近似値を取得
        nearest_idx = self.idx_of_the_nearest(geo_idx, recent_geo)
        # ユーザが直近で更新した日記と位置情報が近似している日記を取得
        diary = list(diaries)[nearest_idx]
        return diary

    def idx_of_the_nearest(self, indexes, values):
        """多次元配列で近似値を探す関数

        indixesが複数のオブジェクト、valuesが一つのオブジェクトとする
        多次元配列は列数がオブジェクトの数、行数がフィールドの数となる
        フィールドの値が数値なら使用可能。
        """
        # モデルのフィールド数
        col = len(values)
        # オブジェクト数
        row = len(indexes[0])
        # オブジェクト数に合った多次元配列作成
        abs_indexes = np.arange(1 * row).reshape((1, row))
        # フィールド数だけ処理
        for val in range(col):
            # 配列作成
            abs_idx = []
            # オブジェクト数だけ処理
            for idx in range(row):
                # オブジェクトごとにフィールドの差分を取得（絶対値）
                abs_value = np.abs(np.array(indexes[val][idx] - values[val]))
                # オブジェクトごとに絶対値の配列作成
                abs_idx = np.append(abs_idx, abs_value)
            # オブジェクトごとの絶対値の配列を多次元配列に変換
            abs_idx = np.expand_dims(abs_idx, 0)
            # オブジェクトごとの絶対値を多次元配列に追加
            abs_indexes = np.append(abs_indexes, abs_idx, axis=0)
        # 最初の行の削除
        abs_indexes = np.delete(abs_indexes, 0, 0)
        # オブジェクトごとの絶対値を足す
        total_col_list = np.sum(abs_indexes, axis=0)
        # 最初に見つかった、最小値のインデックスを取得してint64→intに変換
        nearest_idx = total_col_list.argmin().item()
        return nearest_idx
