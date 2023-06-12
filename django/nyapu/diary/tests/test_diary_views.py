import pytest
from pytest_mock import mocker
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


from diary.filters import MyDiariesFilter, LikedDiariesFilter, RecentDiariesFilter, NearestDiariesFilter
from diary.models import Diary
from accounts.models import CustomUser
from diary.views import DiaryViewSet


class TestDiaryViewSet(APITestCase):# 書きかけ

    @classmethod
    def setUpClass(cls):
        """テストトランザクションの初回処理"""
        #トランザクションを開始するため、必ず親クラスのsetUpClassを最初に呼ぶ
        super().setUpClass()
        # ログインユーザを初期登録
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='user@example.com',
            password='secret',
        )

    def setUp(self):
        """テストメソッドごとの初回処理"""
        # ログイン(JWT認証)
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # 強制的にログイン状態にする
        self.client.force_authenticate(user=self.user)

    @pytest.mark.parametrize(
        'query_params, filter_class',
        [
            ('profile', MyDiariesFilter),
            ('liked_diaries', LikedDiariesFilter),
            ('recent_diaries', RecentDiariesFilter),
            ('nearest_diaries', NearestDiariesFilter),
        ]
    )
    def test_queryset(self, mocker, query_params, filter_class):# Todo なぜかselfを引数として認識しない
        # 一覧取得のテスト
        mocker_filter = mocker.MagicMock()
        mocker.patch.object(filter_class, 'filter_queryset', mocker_filter)

        actual = DiaryViewSet()
        actual.request = self.client.get('diaries/', {query_params: 'true'})
        actual.get_queryset()

        assert mocker_filter.called == True


# import io
# import os
# import pytest
#
# from django.contrib import auth
# from django.contrib.auth import get_user_model
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import TestCase
# from django.urls import reverse_lazy
# from django.conf import settings
#
# from diary.models import Diary, Comment
#
# TEST_USER_DIARY_ID = 101
# NOT_FOUND_DIARY_ID = 999
# IMAGE_FILE_NAME = 'テスト_ベンガル.jpeg'
#
#
# class BaseTestCase(TestCase):
#     """共通の事前準備処理をオーバライドした独自の基底テストクラス"""
#
#     def setUp(self):
#         """テストメソッド実行前の事前設定"""
#         # テストユーザーのパスワード
#         self.password = 'only3100nyapu'
#         # 各インスタンスメソッドで使うテスト用ユーザを生成し
#         # インスタンス変数に格納しておく
#         self.test_user = get_user_model().objects.create_user(
#             username='unittestonly1',
#             email='unittestonly1@example.com',
#             password=self.password)
#         # テスト用ユーザーでログインする
#         self.client.login(username=self.test_user.username, password=self.password)
#         # ログイン状態かを確認
#         assert auth.get_user(self.client).is_authenticated is True
#
#     @staticmethod
#     def _upload_image(file_name=None):
#         """テスト用の画像ファイルを読み込み"""
#         file_path = os.path.join(settings.BASE_DIR, 'media', file_name)
#         # バイナリファイルを読み込みモードでオープン
#         with open(file_path, 'rb') as f:
#             # 画像ファイルをオブジェクトにする
#             file_obj = SimpleUploadedFile(file_name, f.read())
#             return file_obj
#
#
# class TestDiaryCreateView(BaseTestCase):
#     """DiaryCreateView用のテストクラス"""
#
#     def test_create_diary_success(self):
#         """日記作成処理が成功することを検証する"""
#         # Postパラメータ
#         params = {'title': 'テストタイトル',
#                   'content': '本文',
#                   'photo1': self._upload_image(file_name=IMAGE_FILE_NAME),
#                   'photo2': '',
#                   'photo3': '',
#                   'lat': 35.709,
#                   'lon': 139.7319
#                   }
#         # 新規日記作成処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:diary_create'), params)
#         # 日記リストページへのリダイレクトを検証
#         self.assertRedirects(response, reverse_lazy('diary:profile',
#                                                     kwargs={'username': self.test_user}))
#         # 日記データがDBに登録されたかを検証
#         assert Diary.objects.filter(title='テストタイトル').count() == 1
#
#
# class TestDiaryUpdateView(BaseTestCase):
#     """DiaryUpdateView用のテストクラス"""
#
#     def test_update_diary_success(self):
#         """日記編集処理が成功することを検証する"""
#         # テスト用日記データの作成
#         diary = Diary.objects.create(
#             user=self.test_user,
#             title='タイトル編集前',
#             content='本文',
#             lat=35.709,
#             lon=139.7319
#         )
#         # 日記データがDBに登録されたかを検証
#         assert Diary.objects.filter(title='タイトル編集前').count() == 1
#         # Postパラメータ
#         params = {'title': 'タイトル編集後',
#                   'photo1': self._upload_image(file_name=IMAGE_FILE_NAME),
#                   'lat': 35.709,
#                   'lon': 139.7319
#                   }
#         # 日記編集処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:diary_update',
#                                                  kwargs={'pk': diary.pk}), params)
#         # 日記詳細ページへのリダイレクトを検証
#         self.assertRedirects(response, reverse_lazy('diary:diary_detail',
#                                                     kwargs={'pk': diary.pk}))
#         # 日記データが編集されたかを検証
#         assert Diary.objects.filter(title='タイトル編集後').count() == 1
#
#     def test_update_diary_failure(self):
#         """日記編集処理が失敗することを検証する"""
#         # 日記編集処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:diary_update',
#                                                  kwargs={'pk': NOT_FOUND_DIARY_ID}))
#         # 存在しない日記データを編集しようとしてエラーになることを検証
#         assert response.status_code == 404
#
#
# class TestDiaryDeleteView(BaseTestCase):
#     """DiaryDeleteView用のテストクラス"""
#
#     def test_delete_diary_success(self):
#         """日記削除処理が成功することを検証する"""
#         # テスト用日記データの作成
#         diary = Diary.objects.create(user=self.test_user, title='タイトル')
#         # 日記削除処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': diary.pk}))
#         # 日記リストページへのリダイレクトを検証
#         self.assertRedirects(response, reverse_lazy('diary:profile',
#                                                     kwargs={'username': self.test_user}))
#         # 日記データが削除されたかを検証
#         assert Diary.objects.filter(pk=diary.pk).count() == 0
#
#     def test_delete_diary_failure(self):
#         """日記削除処理が失敗することを検証する"""
#         # 日記削除処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:diary_delete',
#                                                  kwargs={'pk': NOT_FOUND_DIARY_ID}))
#         # 存在しない日記データを削除しようとしてエラーになることを検証
#         assert response.status_code == 404
#
#
# class TestCommentCreateView(BaseTestCase):
#     """CommentCreateView用のテストクラス"""
#
#     def test_create_diary_success(self):
#         """コメント作成処理が成功することを検証する"""
#         # テスト用日記データの作成
#         diary = Diary.objects.create(pk=TEST_USER_DIARY_ID, user=self.test_user,
#                                      title="コメントテスト用",
#                                      photo1=self._upload_image(file_name=IMAGE_FILE_NAME))
#         # Postパラメータ
#         params = {'text': 'テストコメント'}
#         # コメント作成処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:comment_create',
#                                                  kwargs={'pk': diary.pk}), params)
#         # 日記リストページへのリダイレクトを検証
#         self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))
#         # コメントデータがDBに登録されたかを検証
#         assert Comment.objects.filter(text='テストコメント', diary__id=diary.pk).count() == 1
#
#     def test_create_diary_failure(self):
#         """コメント作成処理が失敗することを確認する"""
#         # テスト用日記データの作成
#         diary = Diary.objects.create(user=self.test_user,
#                                      title="コメントテスト用",
#                                      photo1=self._upload_image(file_name=IMAGE_FILE_NAME))
#         # コメント作成処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:comment_create', kwargs={'pk': diary.pk}))
#         # 必須フォームフィールドが未入力によりエラーになることを検証
#         self.assertFormError(response, 'form', 'text', 'このフィールドは必須です。')
#
#
# class TestCommentDeleteView(BaseTestCase):
#     """CommentDeleteView用のテストクラス"""
#
#     def test_delete_diary_success(self):
#         """コメント削除処理が成功することを検証する"""
#         # テスト用日記データの作成
#         diary = Diary.objects.create(pk=TEST_USER_DIARY_ID, user=self.test_user,
#                                      title="コメントテスト用",
#                                      photo1=self._upload_image(file_name=IMAGE_FILE_NAME))
#         # テスト用コメントデータの作成
#         comment = Comment.objects.create(diary_id=diary.pk, comment_user=self.test_user,
#                                          text='テストコメント')
#         # コメントデータがDBに登録されたかを検証
#         assert Comment.objects.filter(id=comment.pk).count() == 1
#         # コメント削除処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:comment_delete',
#                                                  kwargs={'pk': comment.pk}))
#         # 日記リストページへのリダイレクトを検証
#         self.assertRedirects(response, reverse_lazy('diary:diary_detail',
#                                                     kwargs={'pk': diary.pk}))
#         # コメントデータがDBから削除されたかを検証
#         assert Comment.objects.filter(id=comment.pk).count() == 0
#
#     def test_delete_diary_failure(self):
#         """コメント削除処理が失敗することを検証する"""
#         # 日記削除処理(Post)を実行
#         response = self.client.post(reverse_lazy('diary:comment_delete',
#                                                  kwargs={'pk': NOT_FOUND_DIARY_ID}), follow=True)
#         # 存在しない日記データを削除しようとしてエラーになることを検証
#         assert response.status_code == 404
