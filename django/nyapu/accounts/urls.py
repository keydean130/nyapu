from django.urls import path, include
from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register('accounts', views.CustomUserViewSet, basename='account')
router.register('follows', views.RelationshipViewSet, basename='follow')

urlpatterns = [
   path('', include(router.urls)),
   path('inquiry/', views.InquiryCreateAPIView.as_view(), name='inquiry'),
]