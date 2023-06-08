from api.serializers import DiarySerializer
from rest_framework import viewsets
from diary.models import Diary

class DiaryViewSet(viewsets.ModelViewSet):
    """日記モデルのCRUD用のAPIクラス"""

    query_set = Diary.objects.all()
    serializer_class = DiarySerializer