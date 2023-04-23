from rest_framework import serializers
from django.nyapu.diary.models import Diary, Comment


class DiarySerializers(serializers.ModelSerializer):
    """日記モデル用シリアライザ"""

    class Meta:
        model = Diary
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3', 'lat', 'lon')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'


class CommentSerializers(serializers.ModelSerializer):
    """コメント用シリアライザ"""

    class Meta:
        model = Comment
        exclude = ('comment_user', 'diary', 'commented_at')
