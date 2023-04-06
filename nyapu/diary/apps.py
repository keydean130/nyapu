from django.apps import AppConfig
from .predictor import Predictor


class DiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diary'

    def ready(self):
        u"""django起動（runserver）時に実行する処理"""
        # 事前学習モデルをインスタンス化してキャッシュしておく
        # pred = Predictor()
        pass


