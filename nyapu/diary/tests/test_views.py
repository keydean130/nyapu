import io

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Diary, Comment
from django.contrib import auth


class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバライドした独自TestCaseクラス"""

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
        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )


class TestDiaryCreateView(LoggedInTestCase):
    """DiaryCreateView用のテストクラス"""

    def _make_dummy_image(self):
        """テスト用の画像ファイルをPILで作成"""
        file_obj = io.BytesIO()
        im = Image.new('RGBA', size=(10, 10), color=(256, 0, 0))
        im.save(file_obj, 'png')
        file_obj.name = 'test.png'
        file_obj.seek(0)
        return file_obj

    def test_create_diary_success(self):
        """日記作成処理が成功することを検証する"""

        # テスト用の画像ファイル
        img = self._make_dummy_image()

        # Postパラメータ
        params = {'title': 'テストタイトル',
                  'content': '本文',
                  'photo1': SimpleUploadedFile(img.name, img.read(), content_type='image/png',),
                  'photo2': '',
                  'photo3': '',
                  'lat': 35.709,
                  'lon': 139.7319
                  }

        # 新規日記作成処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_create'), params)

        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_list', kwargs={'username': self.test_user}))

        # 日記データがDBに登録されたかを検証
        self.assertEqual(Diary.objects.filter(title='テストタイトル').count(), 1)


class TestDiaryUpdateView(LoggedInTestCase):
    """DiaryUpdateView用のテストクラス"""

    def test_update_diary_success(self):
        """日記編集処理が成功することを検証する"""

        # テスト用日記データの作成
        diary = Diary.objects.create(
            user=self.test_user,
            title='タイトル編集前',
            content='本文',
            lat= 35.709,
            lon= 139.7319
        )

        # 日記データがDBに登録されたかを検証
        self.assertEqual(Diary.objects.filter(title='タイトル編集前').count(), 1)

        # Postパラメータ
        params = {'title': 'タイトル編集後', 
                  'lat': 35.709, 
                  'lon': 139.7319
                  }

        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': diary.pk}), params)

        # 日記詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))
    
        # 日記データが編集されたかを検証
        self.assertEqual(Diary.objects.filter(title='タイトル編集後').count(), 1)


    def test_update_diary_failure(self):
        """日記編集処理が失敗することを検証する"""

        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': 999}))

        # 存在しない日記データを編集しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)


class TestDiaryDeleteView(LoggedInTestCase):
    """DiaryDeleteView用のテストクラス"""

    def test_delete_diary_success(self):
        """日記削除処理が成功することを検証する"""

        # テスト用日記データの作成
        diary = Diary.objects.create(user=self.test_user, title='タイトル')

        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': diary.pk}))

        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_list', kwargs={'username': self.test_user}))

        # 日記データが削除されたかを検証
        self.assertEqual(Diary.objects.filter(pk=diary.pk).count(), 0)

    def test_delete_diary_failure(self):
        """日記削除処理が失敗することを検証する"""

        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': 999}))

        # 存在しない日記データを削除しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)


class TestCommentCreateView(LoggedInTestCase):
    """CommentCreateView用のテストクラス"""

    def _make_dummy_image(self):
        """テスト用の画像ファイルをPILで作成"""
        file_obj = io.BytesIO()
        im = Image.new('RGBA', size=(10, 10), color=(256, 0, 0))
        im.save(file_obj, 'png')
        file_obj.name = 'test.png'
        file_obj.seek(0)
        return file_obj

    def test_create_diary_success(self):
        """コメント作成処理が成功することを検証する"""

        # テスト用の画像ファイル
        img = self._make_dummy_image()

        # テスト用日記データの作成
        diary = Diary.objects.create(pk=1000, user=self.test_user, title="コメントテスト用",
                                     photo1=SimpleUploadedFile(img.name, img.read(), content_type='image/png', ))

        # Postパラメータ
        params = {'text': 'テストコメント',
                  'pk': 1000,}

        # コメント作成処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_create', kwargs={'pk': diary.pk}), params)

        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))

        # コメントデータがDBに登録されたかを検証
        self.assertEqual(Comment.objects.filter(text='テストコメント', diary__id=diary.pk).count(), 1)

    def test_create_diary_failure(self):
        """コメント作成処理が失敗することを確認する"""

        # テスト用の画像ファイル
        img = self._make_dummy_image()

        # テスト用日記データの作成
        diary = Diary.objects.create(user=self.test_user, title="コメントテスト用",
                                     photo1=SimpleUploadedFile(img.name, img.read(), content_type='image/png', ))

        # コメント作成処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_create', kwargs={'pk': diary.pk}))

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'text', 'このフィールドは必須です。')


class TestCommentDeleteView(LoggedInTestCase):
    """CommentDeleteView用のテストクラス"""

    def _make_dummy_image(self):
        """テスト用の画像ファイルをPILで作成"""
        file_obj = io.BytesIO()
        im = Image.new('RGBA', size=(10, 10), color=(256, 0, 0))
        im.save(file_obj, 'png')
        file_obj.name = 'test.png'
        file_obj.seek(0)
        return file_obj

    def test_delete_diary_success(self):
        """コメント削除処理が成功することを検証する"""

        # テスト用の画像ファイル
        img = self._make_dummy_image()

        # テスト用日記データの作成
        diary = Diary.objects.create(pk=99, user=self.test_user, title="コメントテスト用",
                                     photo1=SimpleUploadedFile(img.name, img.read(), content_type='image/png', ))

        # テスト用コメントデータの作成
        comment = Comment.objects.create(diary_id=diary.pk, comment_user=self.test_user, text='テストコメント')

        # コメントデータがDBに登録されたかを検証
        self.assertEqual(Comment.objects.filter(id=comment.pk).count(), 1)

        # コメント削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_delete', kwargs={'pk': comment.pk}))

        # 日記リストページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))

        # コメントデータがDBから削除されたかを検証
        self.assertEqual(Comment.objects.filter(id=comment.pk).count(), 0)

    def test_delete_diary_failure(self):
        """コメント削除処理が失敗することを検証する"""

        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:comment_delete', kwargs={'pk': 999}), follow=True)

        # 存在しない日記データを削除しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)

