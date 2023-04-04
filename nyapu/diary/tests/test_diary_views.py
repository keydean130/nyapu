import io
import os
import pytest

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy
from django.conf import settings

from diary.models import Diary, Comment


class BaseTestCase(TestCase):
    """共通の事前準備処理をオーバライドした独自の基底テストクラス"""

    def setUp(self):
        """テストメソッド実行前の事前設定"""
        # テストユーザーのパスワード
        self.password = 'only3100nyapu'
        # 各インスタンスメソッドで使うテスト用ユーザを生成し
        # インスタンス変数に格納しておく
        self.test_user = get_user_model().objects.create_user(
            username='unittestonly1',
            email='unittestonly1@example.com',
            password=self.password)
        # テスト用ユーザーでログインする
        self.client.login(username=self.test_user.username, password=self.password)
        # ログイン状態かを確認
        assert auth.get_user(self.client).is_authenticated is True

    @staticmethod
    def _upload_image(file_name=None):
        """テスト用の画像ファイルを読み込み"""
        img_dir = 'diary/fixtures/test'
        file_path = os.path.join(settings.BASE_DIR, img_dir, file_name)
        # バイナリファイルを読み込みモードでオープン
        with open(file_path, 'rb') as f:
            # 画像ファイルをオブジェクトにする
            file_obj = SimpleUploadedFile(file_name, f.read())
            return file_obj

    def _create_diary(self):
        """テスト用日記の作成"""
        # ユーザーの設定
        guest_user = get_user_model().objects.create_user(
            username='guest1',
            email='guest1@example.com',
            password=self.password)
        Diary.objects.create(
            user=guest_user,
            title='guest1のベンガル',
            content='うちの猫です',
            photo=self._upload_image(file_name='test_bengal.jpg'),
            lat=35.709,
            lon=139.7319
        )
        Diary.objects.create(
            user=guest_user,
            title='guest1のアビシニアン',
            content='うちの猫です',
            photo=self._upload_image(file_name='test_abyssinian.jpg'),
            lat=35.709,
            lon=139.7319
        )


# class TestHomeView(BaseTestCase):
#     """DiaryView用のテストクラス"""
#
#     def test_get_queryset(self):
#         """日記検索処理が成功することを検証する"""
#         # テスト用日記の作成
#         self._create_diary()
#         keyword = 'guest1のベンガル'
#         response = self.client.get(path='', data={'query': keyword})



class TestDiaryCreateView(BaseTestCase):
    """DiaryCreateView用のテストクラス"""

    def test_create_diary_success(self):
        """日記作成処理が成功することを検証する"""
        # Postパラメータ
        params = {'title': 'テストタイトル',
                  'content': '本文',
                  'photo1': self._upload_image(file_name='test_bengal.jpg'),
                  'photo2': '',
                  'photo3': '',
                  'lat': 35.709,
                  'lon': 139.7319
                  }
        # 新規日記作成処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_create'), params)
        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:profile',
                                                    kwargs={'username': self.test_user}))
        # 日記データがDBに登録されたかを検証
        assert Diary.objects.filter(title='テストタイトル').count() == 1


class TestDiaryUpdateView(BaseTestCase):
    """DiaryUpdateView用のテストクラス"""

    def test_update_diary_success(self):
        """日記編集処理が成功することを検証する"""
        # テスト用日記データの作成
        diary = Diary.objects.create(
            user=self.test_user,
            title='タイトル編集前',
            content='本文',
            lat=35.709,
            lon=139.7319
        )
        # 日記データがDBに登録されたかを検証
        assert Diary.objects.filter(title='タイトル編集前').count() == 1
        # Postパラメータ
        params = {'title': 'タイトル編集後',
                  'photo1': self._upload_image(file_name='test_abyssinian.jpg'),
                  'lat': 35.709, 
                  'lon': 139.7319
                  }
        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_update',
                                                 kwargs={'pk': diary.pk}), params)
        # 日記詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail',
                                                    kwargs={'pk': diary.pk}))
        # 日記データが編集されたかを検証
        assert Diary.objects.filter(title='タイトル編集後').count() == 1

    def test_update_diary_failure(self):
        """日記編集処理が失敗することを検証する"""
        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': 999}))
        # 存在しない日記データを編集しようとしてエラーになることを検証
        assert response.status_code == 404


class TestDiaryDeleteView(BaseTestCase):
    """DiaryDeleteView用のテストクラス"""

    def test_delete_diary_success(self):
        """日記削除処理が成功することを検証する"""
        # テスト用日記データの作成
        diary = Diary.objects.create(user=self.test_user, title='タイトル')
        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': diary.pk}))
        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:profile',
                                                    kwargs={'username': self.test_user}))
        # 日記データが削除されたかを検証
        assert Diary.objects.filter(pk=diary.pk).count() == 0

    def test_delete_diary_failure(self):
        """日記削除処理が失敗することを検証する"""
        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': 999}))
        # 存在しない日記データを削除しようとしてエラーになることを検証
        assert response.status_code == 404


class TestCommentCreateView(BaseTestCase):
    """CommentCreateView用のテストクラス"""

    def test_create_diary_success(self):
        """コメント作成処理が成功することを検証する"""
        # テスト用日記データの作成
        diary = Diary.objects.create(pk=1000, user=self.test_user,
                                     title="コメントテスト用",
                                     photo1=self._upload_image(file_name='test_bengal.jpg'))
        # Postパラメータ
        params = {'text': 'テストコメント',
                  'pk': 1000}
        # コメント作成処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_create',
                                                 kwargs={'pk': diary.pk}), params)
        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))
        # コメントデータがDBに登録されたかを検証
        assert Comment.objects.filter(text='テストコメント', diary__id=diary.pk).count() == 1

    def test_create_diary_failure(self):
        """コメント作成処理が失敗することを確認する"""
        # テスト用日記データの作成
        diary = Diary.objects.create(user=self.test_user,
                                     title="コメントテスト用",
                                     photo1=self._upload_image(file_name='test_bengal.jpg'))
        # コメント作成処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_create', kwargs={'pk': diary.pk}))
        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'text', 'このフィールドは必須です。')


class TestCommentDeleteView(BaseTestCase):
    """CommentDeleteView用のテストクラス"""

    def test_delete_diary_success(self):
        """コメント削除処理が成功することを検証する"""
        # テスト用日記データの作成
        diary = Diary.objects.create(pk=99, user=self.test_user,
                                     title="コメントテスト用",
                                     photo1=self._upload_image(file_name='test_bengal.jpg'))
        # テスト用コメントデータの作成
        comment = Comment.objects.create(diary_id=diary.pk, comment_user=self.test_user,
                                         text='テストコメント')
        # コメントデータがDBに登録されたかを検証
        assert Comment.objects.filter(id=comment.pk).count() == 1
        # コメント削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_delete',
                                                 kwargs={'pk': comment.pk}))
        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail',
                                                    kwargs={'pk': diary.pk}))
        # コメントデータがDBから削除されたかを検証
        assert Comment.objects.filter(id=comment.pk).count() == 0

    def test_delete_diary_failure(self):
        """コメント削除処理が失敗することを検証する"""
        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_delete', kwargs={'pk': 999}),
                                    follow=True)
        # 存在しない日記データを削除しようとしてエラーになることを検証
        assert response.status_code == 404
