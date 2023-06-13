import logging
from diary.filters import (LikedDiariesFilter, MyDiariesFilter,
                           NearestDiariesFilter, RecentDiariesFilter)
from diary.models import Diary
from diary.serializers import DiarySerializer
from django_filters import rest_framework as filters
from rest_framework import viewsets

logger = logging.getLogger(__name__)


class DiaryViewSet(viewsets.ModelViewSet):
    """日記モデルのCRUD用のAPIクラス"""
    queryset = Diary.objects.order_by('-created_at')
    serializer_class = DiarySerializer
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
        # プロフィール（自分が投稿した日記）の場合
        if 'profile' in self.request.GET:
            filterset_classes.append(MyDiariesFilter)
        # いいねした日記一覧の場合
        elif 'liked_diaries' in self.request.GET: # Todo URLパラメータにアンスコ使うの良くないらしい
            filterset_classes.append(LikedDiariesFilter)
        # ユーザーが直近に投稿した日記の、猫の品種に基づくおすすめの日記のオブジェクトを取得
        elif 'recent_diaries' in self.request.GET:
            filterset_classes.append(RecentDiariesFilter)
        # ユーザーが直近に投稿した日記の、近所の日記のオブジェクトを取得
        elif 'nearest_diaries' in self.request.GET:
            filterset_classes.append(NearestDiariesFilter)
        return filterset_classes

# class HomeView(LoginRequiredMixin, generic.ListView):
#     """ホームページ用のViewクラス"""
#     model = Diary
#     template_name = 'home.html'
#     paginate_by = 2

#     def get_queryset(self):
#         queryset = Diary.objects.order_by('-created_at')
#         # 検索機能
#         query = self.request.GET.get('query')
#         # titleとcontentから文字列検索する
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query)
#                 | Q(content__icontains=query)
#                 | Q(photo1_most_similar_breed__icontains=query)
#             )
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Like処理
#         diaries = Diary.objects.all()
#         liked_list = []
#         # Like済みの日記のidをliked_listに格納
#         for diary in diaries:
#             liked = diary.like_set.filter(like_user=self.request.user)
#             if liked.exists():
#                 liked_list.append(diary.id)
#             context['liked_list'] = liked_list
#             # コメント数をcountへ格納
#             context['count'] = diary.comment_set.count()
#         # マップ表示用に日記データをmap_diariesに格納   
#         context['map_diaries'] = Diary.objects.all()
#         # おすすめ日記の設定
#         # ユーザと他のユーザが日記をそれぞれ1件以上投稿していれば
#         if all([Diary.objects.exclude(user=self.request.user),
#                 Diary.objects.filter(user=self.request.user)]):
#             # ユーザーが直近で更新した日記のオブジェクトを取得
#             recent_diary = Diary.objects.filter(user=self.request.user).order_by('-updated_at')[0]
#             # ユーザが直近で更新した日記の猫の品種を取得
#             cat_breed = recent_diary.photo1_most_similar_breed
#             # ユーザが直近で更新した日記の猫の品種と同じ、他のユーザが直近で更新した日記があれば
#             if diaries.filter(photo1_most_similar_breed=cat_breed).exclude(
#                     user=self.request.user):
#                 # ユーザが直近で更新した日記の猫の品種と同じ、他のユーザが直近で更新した日記を取得
#                 context['some_cat_breed_diary'] \
#                     = diaries.filter(photo1_most_similar_breed=cat_breed).exclude(
#                     user=self.request.user).order_by('-updated_at')[0]

#             # 他のユーザが直近で更新した日記、最大100件を取得
#             other_user_recent_updated_diaries = Diary.objects.exclude(
#                 user=self.request.user).order_by('-updated_at')[0:99]
#             # ユーザが直近で更新した日記の、最寄りの日記を取得
#             context['nearest_diary'] \
#                 = nearest_diary(recent_diary, other_user_recent_updated_diaries)
#         return context


# class InquiryView(generic.FormView):
#     """お問い合わせページ用のViewクラス"""
#     template_name = 'inquiry.html'
#     form_class = InquiryForm
#     success_url = reverse_lazy('diary:diary')

#     def form_valid(self, form):
#         form.send_email()
#         messages.success(self.request, 'メッセージを送信しました。')
#         logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
#         return super().form_valid(form)


# class ProfileView(LoginRequiredMixin, generic.ListView):
#     """プロフィールページ用のViewクラス"""
#     model = Diary
#     template_name = 'profile.html'
#     paginate_by = 6

#     def get_queryset(self, **kwargs):
#         # ユーザをURLの文字列から取得する
#         user_addr = CustomUser.objects.get(username=self.kwargs['username'])
#         # ユーザの日記のオブジェクトをdiariesへ格納
#         diaries = Diary.objects.filter(user=user_addr).order_by('-created_at')
#         return diaries

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # ユーザをURLの文字列から取得
#         user_addr = CustomUser.objects.get(username=self.kwargs['username'])
#         context['user_addr'] = user_addr
#         # ユーザの投稿数をmy_diary_countへ格納
#         context['my_diary_count'] = Diary.objects.filter(user=user_addr).count()
#         # フォローしているユーザのオブジェクトリストをfollowing_listとして格納
#         context['following_list'] = Relationship.objects.filter(follower_id=user_addr.id)
#         # フォローしているユーザのidリストをfollowingsとして取得
#         followings = (Relationship.objects.filter(follower_id=user_addr.id)).values_list(
#             'following_id')
#         # フォローしているユーザの数をfollowing_countに格納
#         context['following_count'] = CustomUser.objects.filter(id__in=followings).count()
#         # フォロワーのidリストをfollowersとして取得
#         followers = (Relationship.objects.filter(following_id=user_addr.id)).values_list(
#             'follower_id')
#         # フォロワーの数をfollower_countに格納
#         context['follower_count'] = CustomUser.objects.filter(id__in=followers).count()
#         return context


# class LikeDiaryListView(LoginRequiredMixin, generic.ListView):
#     model = Diary
#     template_name = 'like_diary_list.html'
#     paginate_by = 9

#     def get_queryset(self, **kwargs):
#         # ユーザをURLの文字列から取得する
#         user_addr = CustomUser.objects.get(username=self.kwargs['username'])
#         # Like済みの日記のidをliked_diariesとして取得
#         liked_diaries = (Like.objects.filter(like_user=user_addr)).values_list('diary_id')
#         # Like済みの日記のオブジェクトをlike_diary_listに格納
#         like_diary_list = Diary.objects.filter(id__in=liked_diaries)
#         return like_diary_list


# class FollowersView(LoginRequiredMixin, generic.ListView):
#     model = CustomUser
#     template_name = 'followers.html'
#     paginate_by = 9

#     def get_queryset(self):
#         # フォロワーのidリストをfollowersとして取得
#         followers = (Relationship.objects.filter(following_id=self.request.user.id)).values_list(
#             'follower_id')
#         # フォロワーのオブジェクトをfollower_listに格納
#         follower_list = CustomUser.objects.filter(id__in=followers).exclude(
#             username=self.request.user.username)
#         # 検索機能
#         query = self.request.GET.get('query')
#         # usernameとprofileから文字列検索する
#         if query:
#             follower_list = follower_list.filter(
#                 Q(username__icontains=query) | Q(profile__icontains=query)
#             )
#         return follower_list


# class FollowingsView(LoginRequiredMixin, generic.ListView):
#     model = CustomUser
#     template_name = 'followings.html'
#     paginate_by = 9

#     def get_queryset(self):
#         # フォローしているユーザのidをfollowingsに格納
#         followings = Relationship.objects.filter(follower=self.request.user.id).values_list(
#             'following_id')
#         # フォローしているユーザのオブジェクトリストをfollowing_listとして格納
#         following_list = CustomUser.objects.filter(id__in=followings).exclude(
#             username=self.request.user.username)
#         # 検索機能
#         query = self.request.GET.get('query')
#         # usernameとprofileから文字列検索する
#         if query:
#             following_list = following_list.filter(
#                 Q(username__icontains=query) | Q(profile__icontains=query)
#             )
#         return following_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # ログインユーザ以外のユーザのオブジェクトを取得
#         alluser_list = CustomUser.objects.all().exclude(id=self.request.user.id)
#         context['alluser_list'] = alluser_list
#         # フォローしているユーザのidをfollowed_listに格納
#         followed_list = []
#         for item in alluser_list:
#             followed = Relationship.objects.filter(following=item.id, follower=self.request.user)
#             if followed.exists():
#                 followed_list.append(item.id)
#         context['followed_list'] = followed_list
#         return context


# class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Diary
#     template_name = 'diary_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Like処理
#         diaries = Diary.objects.all()
#         liked_list = []
#         # Like済みの日記のidをliked_listに格納
#         for diary in diaries:
#             liked = diary.like_set.filter(like_user=self.request.user)
#             if liked.exists():
#                 liked_list.append(diary.id)
#         context['liked_list'] = liked_list
#         # 日記のコメントのオブジェクトをcommentsに格納
#         context['comments'] = Comment.objects.filter(diary_id=self.kwargs['pk'])
#         return context


# class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Diary
#     template_name = 'diary_create.html'
#     form_class = DiaryCreateForm

#     def get_success_url(self):
#         return reverse_lazy('diary:profile', kwargs={'username': self.request.user})

#     def form_valid(self, form):
#         diary = form.save(commit=False)
#         # 画像分類の処理
#         pred = Predictor()
#         diary = pred.predict(diary, 3)
#         diary.user = self.request.user
#         diary.save()
#         messages.success(self.request, '日記を作成しました。')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, '日記の作成に失敗しました。')
#         return super().form_invalid(form)


# class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
#     model = Diary
#     template_name = 'diary_update.html'
#     form_class = DiaryCreateForm

#     def get_success_url(self):
#         return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

#     def form_valid(self, form):
#         diary = form.save(commit=False)
#         # 画像分類の処理
#         pred = Predictor()
#         diary = pred.predict(diary, 3)
#         diary.user = self.request.user
#         diary.save()
#         messages.success(self.request, '日記を更新しました。')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, '日記の更新に失敗しました。')
#         return super().form_invalid(form)


# class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
#     model = Diary
#     template_name = 'diary_delete.html'

#     def get_success_url(self):
#         return reverse_lazy('diary:profile', kwargs={'username': self.request.user})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # 日記を取得
#         diary = get_object_or_404(Diary, pk=self.kwargs['pk'])
#         context['diary'] = diary
#         return context

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, '日記を削除しました。')
#         return super().delete(request, args, **kwargs)


# class MapView(LoginRequiredMixin, generic.ListView):
#     model = Diary
#     template_name = 'map.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['map_diaries'] = Diary.objects.all()
#         return context


# class MappingView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         # 辞書型のリスト型に仕立てる。
#         map_diaries = list(Diary.objects.all().values())
#         # contextと同じように辞書型にさせる
#         json = {
#             'map_diaries': map_diaries,
#         }
#         return JsonResponse(json)

#     def post(self, request, *args, **kwargs):
#         form = DiaryCreateForm(request.POST)
#         if form.is_valid():
#             print('OK')
#             form.save()
#         return redirect('diary:diary')


# def like_func(request):
#     if request.method == 'POST':
#         # 日記を取得
#         diary = get_object_or_404(Diary, pk=request.POST.get('diary_id'))
#         # Like処理
#         like_user = request.user
#         liked = False
#         like = Like.objects.filter(diary=diary, like_user=like_user)
#         # 日記をLike済みの場合、Likeを削除する
#         if like.exists():
#             like.delete()
#         # 日記をLikeしていない場合、Likeを作成する
#         else:
#             like.create(diary=diary, like_user=like_user)
#             liked = True

#         context = {
#             'diary_id': diary.id,
#             'liked': liked,
#             'count': diary.like_set.count(),
#         }
#         return JsonResponse(context)


# def follow_func(request):
#     if request.method == 'POST':
#         # 対象ユーザを取得
#         item = get_object_or_404(CustomUser, pk=request.POST.get('item_id'))
#         # フォロー処理
#         follower = request.user
#         followed = False
#         follow = Relationship.objects.filter(following=item, follower=follower)
#         # ユーザをフォロー済みの場合、アンフォロー（フォロー削除）する
#         if follow.exists():
#             follow.delete()
#         # ユーザをフォロー済みの場合、フォロー（フォロー作成）する
#         else:
#             follow.create(following=item, follower=follower)
#             followed = True
#         context = {
#             'item_id': item.id,
#             'followed': followed,
#         }
#         return JsonResponse(context)


# class CommentCreate(LoginRequiredMixin, generic.CreateView):
#     template_name = 'comment_form.html'
#     model = Comment
#     form_class = CommentCreateForm

#     def form_valid(self, form):
#         diary_pk = self.kwargs['pk']
#         diary = get_object_or_404(Diary, pk=diary_pk)
#         comment = form.save(commit=False)
#         comment.diary = diary
#         comment.comment_user = self.request.user
#         comment.save()
#         return redirect('diary:diary_detail', pk=diary_pk)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # 日記を取得
#         diary = get_object_or_404(Diary, pk=self.kwargs['pk'])
#         context['diary'] = diary
#         # 日記のコメントのオブジェクトをcommentsに格納
#         context['comments'] = Comment.objects.filter(diary=diary.id)
#         return context


# class CommentDelete(LoginRequiredMixin, generic.DeleteView):
#     model = Comment
#     template_name = 'comment_delete.html'

#     def get_success_url(self, **kwargs):
#         comment = (Comment.objects.get(id=self.kwargs['pk']))
#         return reverse_lazy('diary:diary_detail', kwargs={'pk': comment.diary_id})

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, 'コメントを削除しました。')
#         return super().delete(request, args, **kwargs)


# def idx_of_the_nearest(indexes, values):
#     """多次元配列で近似値を探す関数

#     indixesが複数のオブジェクト、valuesが一つのオブジェクトとする
#     多次元配列は列数がオブジェクトの数、行数がフィールドの数となる
#     フィールドの値が数値なら使用可能。
#     """
#     # モデルのフィールド数
#     col = len(values)
#     # オブジェクト数
#     row = len(indexes[0])
#     # オブジェクト数に合った多次元配列作成
#     abs_indexes = np.arange(1 * row).reshape((1, row))
#     # フィールド数だけ処理
#     for val in range(col):
#         # 配列作成
#         abs_idx = []
#         # オブジェクト数だけ処理
#         for idx in range(row):
#             # オブジェクトごとにフィールドの差分を取得（絶対値）
#             abs_value = np.abs(np.array(indexes[val][idx] - values[val]))
#             # オブジェクトごとに絶対値の配列作成
#             abs_idx = np.append(abs_idx, abs_value)
#         # オブジェクトごとの絶対値の配列を多次元配列に変換
#         abs_idx = np.expand_dims(abs_idx, 0)
#         # オブジェクトごとの絶対値を多次元配列に追加
#         abs_indexes = np.append(abs_indexes, abs_idx, axis=0)
#     # 最初の行の削除
#     abs_indexes = np.delete(abs_indexes, 0, 0)
#     # オブジェクトごとの絶対値を足す
#     total_col_list = np.sum(abs_indexes, axis=0)
#     # 最初に見つかった、最小値のインデックスを取得してint64→intに変換
#     nearest_idx = total_col_list.argmin().item()
#     return nearest_idx


# def nearest_diary(diary, diaries):
#     # diaryの位置情報の配列作成
#     recent_geo = [diary.lat, diary.lon]
#     # diariesの位置情報の配列作成
#     lat_idx = []
#     lon_idx = []
#     # クエリ―セットでオブジェクトの指定要素のみを取得
#     for d_lat, d_lon in zip(diaries.values_list('lat'),
#                             diaries.values_list('lon')):
#         # タプルから要素を取り出して配列に格納
#         lat_idx.append(d_lat[0])
#         lon_idx.append(d_lon[0])
#     # 位置情報の配列を設定
#     geo_idx = [lat_idx, lon_idx]
#     # 近似値を取得
#     nearest_idx = idx_of_the_nearest(geo_idx, recent_geo)
#     # ユーザが直近で更新した日記と位置情報が近似している日記を取得
#     diary = list(diaries)[nearest_idx]
#     return diary
