import logging

from accounts.filters import (CustomUsersFilter, FollowersFilter,
                              FollowingsFilter)
from accounts.models import CustomUser, Relationship
from accounts.serializers import (CustomUserSerializer, InquirySerializer,
                                  RelationshipSerializer)
from django_filters import rest_framework as filters
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    """カスタムユーザーモデルのCRUD用のAPIクラス"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CustomUsersFilter


class RelationshipViewSet(viewsets.ModelViewSet):
    """フォローモデルのCRUD用のAPIクラス"""
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        queryset = super().get_queryset()
        filterset_classes = self.get_filterset_classes()
        # 設定された分、フィルタ―する
        if filterset_classes:
            for filterset_class in filterset_classes:
                filterset = filterset_class(self.request.GET, queryset=queryset)
                queryset = filterset.qs
        return queryset

    def get_filterset_classes(self):
        """URLパラメータによって使用するfiletersetクラスを決める（複数可）"""
        filterset_classes = []
        # ログインユーザをフォローしているユーザー一覧取得の場合
        if 'followers' in self.request.GET:
            filterset_classes.append(FollowersFilter)
        # ログインユーザがフォローしているユーザー一覧取得の場合
        elif 'followings' in self.request.GET:
            filterset_classes.append(FollowingsFilter)
        else:
            pass
        return filterset_classes


class InquiryCreateAPIView(generics.CreateAPIView):
    """お問い合わせページ用のViewクラス"""
    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        """お問い合わせフォームの作成"""
        # シリアライザからリクエストデータを取得
        serializer = self.get_serializer(data=request.data)
        # リクエストデータの検証
        serializer.is_valid(raise_exception=True)
        # お問い合わせのメール送信
        serializer.send_email()
        return Response({'message': 'メッセージを送信しました。'}, status=status.HTTP_201_CREATED)    
