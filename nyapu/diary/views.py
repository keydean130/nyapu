import logging

from accounts.models import Relationship, CustomUser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from .forms import InquiryForm, DiaryCreateForm, CommentCreateForm
from .models import Diary, Like, Comment

logger = logging.getLogger(__name__)


class DiaryView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Diary.objects.order_by('-created_at')
        # 検索機能
        query = self.request.GET.get('query')
        # titleとcontentから文字列検索する
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):  # 追加
        context = super().get_context_data(**kwargs)
        # Like処理
        diaries = Diary.objects.all()
        liked_list = []
        # Like済みの日記のidをliked_listに格納
        for diary in diaries:
            liked = diary.like_set.filter(like_user=self.request.user)
            if liked.exists():
                liked_list.append(diary.id)
        context["liked_list"] = liked_list
        # コメント数をcomment_countへ格納
        context["count"] = diary.comment_set.count()
        # マップ表示用に日記データをmap_diariesに格納   
        context['map_diaries'] = Diary.objects.all()
        return context


class InquiryView(generic.FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('diary:diary')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        # ユーザをURLの文字列から取得する
        user_addr = CustomUser.objects.get(username=self.kwargs['username'])
        # ユーザの日記のオブジェクトをdiariesへ格納
        diaries = Diary.objects.filter(user=user_addr).order_by('-created_at')
        return diaries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ユーザをURLの文字列から取得
        user_addr = CustomUser.objects.get(username=self.kwargs['username'])
        context['user_addr'] = user_addr
        # ユーザの投稿数をmy_diary_countへ格納
        context['my_diary_count'] = Diary.objects.filter(user=user_addr).count()
        # フォローしているユーザのオブジェクトリストをfollowing_listとして格納
        context['following_list'] = Relationship.objects.filter(follower_id=user_addr.id)
        # フォローしているユーザのidリストをfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user_addr.id)).values_list(
            'following_id')
        # フォローしているユーザの数をfollowing_countに格納
        context['following_count'] = CustomUser.objects.filter(id__in=followings).count()
        # フォロワーのidリストをfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user_addr.id)).values_list(
            'follower_id')
        # フォロワーの数をfollower_countに格納
        context['follower_count'] = CustomUser.objects.filter(id__in=followers).count()
        return context


class LikeDiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'like_diary_list.html'
    paginate_by = 9

    def get_queryset(self, **kwargs):
        # ユーザをURLの文字列から取得する
        user_addr = CustomUser.objects.get(username=self.kwargs['username'])
        # Like済みの日記のidをliked_diariesとして取得
        liked_diaries = (Like.objects.filter(like_user=user_addr)).values_list('diary_id')
        # Like済みの日記のオブジェクトをlike_diary_listに格納
        like_diary_list = Diary.objects.filter(id__in=liked_diaries)
        return like_diary_list


class FollowersView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'followers.html'
    paginate_by = 3

    def get_queryset(self):
        # フォロワーのidリストをfollowersとして取得
        followers = (Relationship.objects.filter(following_id=self.request.user.id)).values_list(
            'follower_id')
        # フォロワーのオブジェクトをfollower_listに格納
        follower_list = CustomUser.objects.filter(id__in=followers).exclude(
            username=self.request.user.username)
        # 検索機能
        query = self.request.GET.get('query')
        # usernameとprofileから文字列検索する
        if query:
            follower_list = follower_list.filter(
                Q(username__icontains=query)|Q(profile__icontains=query)
            )
        return follower_list


class FollowingsView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'followings.html'
    paginate_by = 3

    def get_queryset(self):
        # フォローしているユーザのidをfollowingsに格納
        followings = Relationship.objects.filter(follower=self.request.user.id).values_list(
            'following_id')
        # フォローしているユーザのオブジェクトリストをfollowing_listとして格納
        following_list = CustomUser.objects.filter(id__in=followings).exclude(
            username=self.request.user.username)
        # 検索機能
        query = self.request.GET.get('query')
        # usernameとprofileから文字列検索する
        if query:
            following_list = following_list.filter(
                Q(username__icontains=query)|Q(profile__icontains=query)
            )
        return following_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザ以外のユーザのオブジェクトを取得
        alluser_list = CustomUser.objects.all().exclude(id=self.request.user.id)
        context['alluser_list'] = alluser_list
        # フォローしているユーザのidをfollowed_listに格納
        followed_list = []
        for item in alluser_list:
            followed = Relationship.objects.filter(following=item.id, follower=self.request.user)
            if followed.exists():
                followed_list.append(item.id)
        context['followed_list'] = followed_list
        return context


class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Like処理
        diaries = Diary.objects.all()
        liked_list = []
        # Like済みの日記のidをliked_listに格納
        for diary in diaries:
            liked = diary.like_set.filter(like_user=self.request.user)
            if liked.exists():
                liked_list.append(diary.id)
        context["liked_list"] = liked_list
        # 日記のコメントのオブジェクトをcommentsに格納
        context["comments"] = Comment.objects.filter(diary_id=self.kwargs["pk"])

        return context


class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_list', kwargs={'username': self.request.user})

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)


class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)


class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'

    def get_success_url(self):
        return reverse_lazy('diary:diary_list', kwargs={'username': self.request.user})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 日記を取得
        diary = get_object_or_404(Diary, pk=self.kwargs['pk'])
        context["diary"] = diary
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, args, **kwargs)


class MapView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map_diaries'] = Diary.objects.all()
        return context


class MappingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 辞書型のリスト型に仕立てる。
        map_diaries = list(Diary.objects.all().values())
        # contextと同じように辞書型にさせる
        json = {
            "map_diaries": map_diaries,
        }
        return JsonResponse(json)

    def post(self, request):
        form = DiaryCreateForm(request.POST)
        if form.is_valid():
            print("OK")
            form.save()
        return redirect("diary:diary")


def like_func(request):
    if request.method == "POST":
        # 日記を取得
        diary = get_object_or_404(Diary, pk=request.POST.get('diary_id'))
        # Like処理
        like_user = request.user
        liked = False
        like = Like.objects.filter(diary=diary, like_user=like_user)
        # 日記をLike済みの場合、Likeを削除する
        if like.exists():
            like.delete()
        # 日記をLikeしていない場合、Likeを作成する
        else:
            like.create(diary=diary, like_user=like_user)
            liked = True

        context = {
            'diary_id': diary.id,
            'liked': liked,
            'count': diary.like_set.count(),
        }
        return JsonResponse(context)


def follow_func(request):
    if request.method == "POST":
        # 対象ユーザを取得
        item = get_object_or_404(CustomUser, pk=request.POST.get('item_id'))
        # フォロー処理
        follower = request.user
        followed = False
        follow = Relationship.objects.filter(following=item, follower=follower)
        # ユーザをフォロー済みの場合、アンフォロー（フォロー削除）する
        if follow.exists():
            follow.delete()
        # ユーザをフォロー済みの場合、フォロー（フォロー作成）する
        else:
            follow.create(following=item, follower=follower)
            followed = True
        context = {
            'item_id': item.id,
            'followed': followed,
        }
        return JsonResponse(context)


class CommentCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        diary_pk = self.kwargs['pk']
        diary = get_object_or_404(Diary, pk=diary_pk)
        comment = form.save(commit=False)
        comment.diary = diary
        comment.comment_user = self.request.user
        comment.save()
        return redirect('diary:diary_detail', pk=diary_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 日記を取得
        diary = get_object_or_404(Diary, pk=self.kwargs['pk'])
        context["diary"] = diary
        # 日記のコメントのオブジェクトをcommentsに格納
        context["comments"] = Comment.objects.filter(diary=diary.id)
        return context


class CommentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self, **kwargs):
        comment = (Comment.objects.get(id=self.kwargs["pk"]))
        return reverse_lazy('diary:diary_detail', kwargs={'pk': comment.diary_id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "コメントを削除しました。")
        return super().delete(request, args, **kwargs)
