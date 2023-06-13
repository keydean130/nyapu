from django.urls import path, include
from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register('accounts', views.CustomUserViewSet, basename='account')
router.register('follows', views.RelationshipViewSet, basename='follow')

urlpatterns = [
   path('', include(router.urls)),
   # path('edit_profile/', views.ProfileEditView.as_view(), name="edit_profile"),
   # path('userlist/', views.UserListView.as_view(), name="userlist"),
]