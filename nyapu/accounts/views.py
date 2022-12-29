from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from .forms import ProfileForm
from .models import CustomUser, Relationship


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'account/edit_profile.html'
    model = CustomUser
    form_class = ProfileForm
    success_url = '/accounts/edit_profile/'

    def get_object(self):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    template_name = 'account/userlist.html'
    model = CustomUser
    paginate_by = 3

    def get_queryset(self):
        alluser_list = CustomUser.objects.all().exclude(id=self.request.user.id)
                        
        # 検索機能
        query = self.request.GET.get('query')

        # usernameとprofileから文字列検索する
        if query:
            alluser_list = alluser_list.filter(
                Q(username__icontains=query)|Q(profile__icontains=query)
            )
        return alluser_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザ以外のユーザのオブジェクトを取得
        alluser_list = CustomUser.objects.all().exclude(id=self.request.user.id)
        # フォローしているユーザのidをfollowed_listに格納
        followed_list = []
        for item in alluser_list:
            followed = Relationship.objects.filter(following=item.id, follower=self.request.user)
            if followed.exists():
                followed_list.append(item.id)
        context['followed_list'] = followed_list
        return context


