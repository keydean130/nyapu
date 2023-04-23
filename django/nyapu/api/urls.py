from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('diaries', views.DiaryViewSet)

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls))
]