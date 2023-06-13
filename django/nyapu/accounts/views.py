import logging

from accounts.filters import FollowersFilter, FollowingsFilter
from accounts.models import CustomUser, Relationship
from accounts.serializers import CustomUserSerializer, RelationshipSerializer
from django_filters import rest_framework as filters
from rest_framework import viewsets

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    """カスタムユーザーモデルのCRUD用のAPIクラス"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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


#
# class ProfileEditView(LoginRequiredMixin, UpdateView):
#     template_name = 'account/edit_profile.html'
#     model = CustomUser
#     form_class = ProfileForm
#     success_url = '/accounts/edit_profile/'
#
#     def get_object(self):
#         return self.request.user
#
#
# class UserListView(LoginRequiredMixin, ListView):
#     template_name = 'account/userlist.html'
#     model = CustomUser
#     paginate_by = 9
#
#     def get_queryset(self):
#         alluser_list = CustomUser.objects.all().exclude(id=self.request.user.id)
#         # 検索機能
#         query = self.request.GET.get('query')
#         # usernameとprofileから文字列検索する
#         if query:
#             alluser_list = alluser_list.filter(
#                 Q(username__icontains=query)|Q(profile__icontains=query)
#             )
#         return alluser_list
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # ログインユーザ以外のユーザのオブジェクトを取得
#         alluser_list = CustomUser.objects.all().exclude(id=self.request.user.id)
#         # フォローしているユーザのidをfollowed_listに格納
#         followed_list = []
#         for item in alluser_list:
#             followed = Relationship.objects.filter(following=item.id, follower=self.request.user)
#             if followed.exists():
#                 followed_list.append(item.id)
#         context['followed_list'] = followed_list
#         return context
#
#
