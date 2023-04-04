
import pytest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


LOGIN_USER_ID = 10
LOGIN_USER_DIARY_ID = 100
OTHER_USER_ID = 11
OTHER_USER_DIARY_ID = 101
OTHER_USER_DIARY_TITLE = '二つ目の日記本文'


class UiTest(StaticLiveServerTestCase):
    """UIテストクラス

    メソッド名のtestの後の数字で実行順序が決まる
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        # サンドボックスモード解除
        options.add_argument('--no-sandbox')
        # GPU無効化
        options.add_argument('--disable-gpu')
        # seleniumドライバーの設定（seleniumコンテナから実行する）
        cls.selenium = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub', options=options,
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_1_login(self):
        """ログイン機能を検証する"""
        # ログインページを開く
        self.selenium.get('http://nyapu:8000')
        # 管理者権限のあるユーザでログイン
        email_input = self.selenium.find_element(By.NAME, 'login')
        email_input.send_keys('uitest1@gmail.com')
        password_input = self.selenium.find_element(By.NAME, 'password')
        password_input.send_keys('onlynyapu')
        self.selenium.find_element(By.NAME, 'btn').click()
        # ページタイトルの検証
        assert self.selenium.title == 'トップページ ｜ にゃっぷ'

    def test_2_like(self):
        """いいね機能を検証する"""
        # いいね処理の待ち時間
        wait = WebDriverWait(self.selenium, 10)
        # トップページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:home')))
        # 日記のキーワード検索
        query_input = self.selenium.find_element(By.NAME, 'query')
        query_input.send_keys(OTHER_USER_DIARY_TITLE)
        self.selenium.find_element(By.NAME, 'search').click()
        # 全画面表示にする（ボタンが画面から見切れる場合が多いため）
        self.selenium.maximize_window()
        # APIの通信が完了するまで待つ(未いいね)
        like_none_element = wait.until(EC.presence_of_element_located(
            (By.NAME, '%s-like-none' % str(OTHER_USER_DIARY_ID))), message='')
        # 日記へのいいね
        like_none_element.like_button_element = self.selenium.find_element(
            By.NAME, str(OTHER_USER_DIARY_ID))
        like_none_element.like_button_element.send_keys(Keys.ENTER)
        # APIの通信が完了するまで待つ(いいね済み)
        like_red_element = wait.until(EC.presence_of_element_located(
            (By.NAME, '%s-like-red' % str(OTHER_USER_DIARY_ID))), message='')
        # 日記詳細ページを開く
        self.selenium.get('http://nyapu:8000'
                          + str(reverse_lazy('diary:diary_detail',
                                             kwargs={'pk': OTHER_USER_DIARY_ID})))
        # 全画面表示にする（ボタンが画面から見切れる場合が多いため）
        self.selenium.maximize_window()
        # APIの通信が完了するまで待つ(いいね済み)
        like_red_element = wait.until(EC.presence_of_element_located(
            (By.NAME, '%s-like-red' % str(OTHER_USER_DIARY_ID))), message='')
        # 日記へのいいね解除
        like_red_element.like_button_element = self.selenium.find_element(
            By.NAME, str(OTHER_USER_DIARY_ID))
        like_red_element.like_button_element.send_keys(Keys.ENTER)

    def test_3_follow(self):
        """フォロー機能を検証する"""
        # フォロー処理の待ち時間
        wait = WebDriverWait(self.selenium, 10)
        # ユーザリストページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('accounts:userlist')))
        # ユーザーのキーワード検索
        query_input = self.selenium.find_element(By.NAME, 'query')
        query_input.send_keys('testonly')
        self.selenium.find_element(By.NAME, 'search').click()
        # APIの通信が完了するまで待つ(未フォロー)
        unfollowed_element = wait.until(
            EC.presence_of_element_located(
                (By.NAME, '%s-follow-none' % str(OTHER_USER_ID))), message='')
        # ユーザーのフォロー
        unfollowed_element.follow_button_element = self.selenium.find_element(
            By.NAME, str(OTHER_USER_ID))
        unfollowed_element.follow_button_element.send_keys(Keys.ENTER)
        # フォローリストページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:followings')))
        # ユーザーのキーワード検索
        query_input = self.selenium.find_element(By.NAME, 'query')
        query_input.send_keys('testonly')
        self.selenium.find_element(By.NAME, 'search').click()
        # APIの通信が完了するまで待つ(フォロー済み)
        followed_element = wait.until(EC.presence_of_element_located(
            (By.NAME, '%s-follow' % str(OTHER_USER_ID))), message='')
        # ユーザーのアンフォロー
        followed_element.follow_button_element = self.selenium.find_element(
            By.NAME, str(OTHER_USER_ID))
        followed_element.follow_button_element.send_keys(Keys.ENTER)

    def test_4_map(self):
        """地図機能を検証する"""
        # 地図処理の待ち時間
        wait = WebDriverWait(self.selenium, 10)
        # 地図ページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:map')))
        # 全画面表示にする（ボタンが画面から見切れる場合が多いため）
        self.selenium.maximize_window()
        # ページタイトルの検証
        assert self.selenium.title == 'にゃっぷ | にゃっぷ'
        # APIの通信が完了するまで待つ
        map_element = wait.until(EC.presence_of_element_located((By.NAME, 'diary_d')), message='')
        # 日記を見るボタンをクリック
        map_element.diary_button_element = self.selenium.find_element(By.NAME, 'diary_d')
        map_element.diary_button_element.send_keys(Keys.ENTER)
        # ページタイトルの検証
        assert self.selenium.title == '日記詳細 | にゃっぷ'
        # トップページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:home')))
        # 全画面表示にする（ボタンが画面から見切れる場合が多いため）
        self.selenium.maximize_window()
        # ページタイトルの検証
        assert self.selenium.title == 'トップページ ｜ にゃっぷ'
        # APIの通信が完了するまで待つ
        # 日記を見るボタンをクリック
        map_element.diary_button_element = self.selenium.find_elements(By.NAME, 'diary_d')
        map_element.diary_button_element[1].send_keys(Keys.ENTER)
        # ページタイトルの検証
        assert self.selenium.title == '日記詳細 | にゃっぷ'
