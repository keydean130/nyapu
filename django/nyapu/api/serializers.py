from rest_framework import serializers
from diary.models import Diary


class DiarySerializer(serializers.ModelSerializer):
    """日記モデル用シリアライザ"""

    class Meta:
        model = Diary
        fields = '__all__'