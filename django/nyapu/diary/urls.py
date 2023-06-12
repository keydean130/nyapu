from django.urls import path, include
from rest_framework import routers

from diary import views

router = routers.DefaultRouter()
router.register('diaries', views.DiaryViewSet, basename='diary')

urlpatterns = [
    path('', include(router.urls))
    # path('', views.HomeView.as_view(), name='home'),
    # path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    # path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    # path('like-diary-list/<str:username>/', views.LikeDiaryListView.as_view(),
    #      name='like_diary_list'),
    # path('diary-detail/<int:pk>/', views.DiaryDetailView.as_view(), name='diary_detail'),
    # path('diary-create/', views.DiaryCreateView.as_view(), name='diary_create'),
    # path('diary-update/<int:pk>/', views.DiaryUpdateView.as_view(), name='diary_update'),
    # path('diary-delete/<int:pk>/', views.DiaryDeleteView.as_view(), name='diary_delete'),
    # path('followers/', views.FollowersView.as_view(), name='followers'),
    # path('followings/', views.FollowingsView.as_view(), name='followings'),
    # path('map/', views.MapView.as_view(), name='map'),
    # path('mapping/', views.MappingView.as_view(), name='mapping'),
    # path('like', views.like_func, name='like'),
    # path('follow', views.follow_func, name='follow'),
    # path('comment-create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    # path('comment-delete/<int:pk>/', views.CommentDelete.as_view(), name='comment_delete'),
]