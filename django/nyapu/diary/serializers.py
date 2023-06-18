from diary.models import Diary
from rest_framework import serializers


class DiarySerializer(serializers.ModelSerializer):
    """日記モデル用シリアライザ"""

    class Meta:
        model = Diary
        fields = ['user', 'id', 'title', 'content', 'photo1']
