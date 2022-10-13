from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait

class UiTest(StaticLiveServerTestCase):
    fixtures = ['test/test_view.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()     
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox') 
        options.add_argument('--disable-gpu') 

        cls.selenium = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options = options,
        )
  
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_1(self):
        """ログイン機能を検証する"""

        # ログインページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('account_login')))

        # 管理者権限のあるユーザでログイン
        email_input = self.selenium.find_element(By.NAME, "login")
        email_input.send_keys('testonly@example.com')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('onlynyapu')

        self.selenium.find_element(By.NAME, "btn").click()

        # ページタイトルの検証
        self.assertEquals('トップページ ｜ にゃっぷ', self.selenium.title)


    def test_2(self):
        """いいね機能を検証する"""

        # いいね処理の待ち時間
        wait = WebDriverWait(self.selenium, 10)

        # トップページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:diary')))

        # 日記のキーワード検索
        query_input = self.selenium.find_element(By.NAME, "query")
        query_input.send_keys('一つ目の日記本文')
        self.selenium.find_element(By.NAME, "search").click()

        # APIの通信が完了するまで待つ(未いいね)
        like_none_element = wait.until(EC.presence_of_element_located((By.NAME, '100-like-none')), message="")

        # 日記へのいいね
        like_none_element.like_button_element = self.selenium.find_element(By.NAME, '100')
        like_none_element.like_button_element.send_keys(Keys.ENTER)

        # APIの通信が完了するまで待つ(いいね済み)
        like_red_element = wait.until(EC.presence_of_element_located((By.NAME, '100-like-red')), message="")

        # 日記へのいいね解除
        like_red_element.like_button_element = self.selenium.find_element(By.NAME, '100')
        like_red_element.like_button_element.send_keys(Keys.ENTER)

        # 日記詳細ページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:diary_detail', kwargs={'pk': 100})))

        # APIの通信が完了するまで待つ(未いいね)
        like_none_element = wait.until(EC.presence_of_element_located((By.NAME, '100-like-none')), message="")

        # 日記へのいいね
        like_none_element.like_button_element = self.selenium.find_element(By.NAME, '100')
        like_none_element.like_button_element.send_keys(Keys.ENTER)

        # APIの通信が完了するまで待つ(いいね済み)
        like_red_element = wait.until(EC.presence_of_element_located((By.NAME, '100-like-red')), message="")

        # 日記へのいいね解除
        like_red_element.like_button_element = self.selenium.find_element(By.NAME, '100')
        like_red_element.like_button_element.send_keys(Keys.ENTER)


    def test_3(self):
        """フォロー機能を検証する"""

        # フォロー処理の待ち時間
        wait = WebDriverWait(self.selenium, 10)

        # ユーザリストページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('accounts:userlist')))

        # 日記のキーワード検索
        query_input = self.selenium.find_element(By.NAME, "query")
        query_input.send_keys('uitest1')
        self.selenium.find_element(By.NAME, "search").click()

        # APIの通信が完了するまで待つ(未フォロー)
        unfollowed_element = wait.until(EC.presence_of_element_located((By.NAME, '100-follow-none')), message="")

        # ユーザーのフォロー
        unfollowed_element.follow_button_element = self.selenium.find_element(By.NAME, '100')
        unfollowed_element.follow_button_element.send_keys(Keys.ENTER)

        # APIの通信が完了するまで待つ(フォロー済み)
        followed_element = wait.until(EC.presence_of_element_located((By.NAME, '100-follow')), message="")

        # ユーザーのアンフォロー
        followed_element.follow_button_element = self.selenium.find_element(By.NAME, '100')
        followed_element.follow_button_element.send_keys(Keys.ENTER)

        # フォローリストに表示させるために再度フォロー
        # APIの通信が完了するまで待つ(未フォロー)
        unfollowed_element = wait.until(EC.presence_of_element_located((By.NAME, '100-follow-none')), message="")

        # ユーザーのフォロー
        unfollowed_element.follow_button_element = self.selenium.find_element(By.NAME, '100')
        unfollowed_element.follow_button_element.send_keys(Keys.ENTER)

        # フォローリストページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:followings')))

        # 日記のキーワード検索
        query_input = self.selenium.find_element(By.NAME, "query")
        query_input.send_keys('uitest1')
        self.selenium.find_element(By.NAME, "search").click()

        # APIの通信が完了するまで待つ(フォロー済み)
        followed_element = wait.until(EC.presence_of_element_located((By.NAME, '100-follow')), message="")

        # ユーザーのアンフォロー
        followed_element.follow_button_element = self.selenium.find_element(By.NAME, '100')
        followed_element.follow_button_element.send_keys(Keys.ENTER)

        # APIの通信が完了するまで待つ(未フォロー)
        unfollowed_element = wait.until(EC.presence_of_element_located((By.NAME, '100-follow-none')), message="")

        # ユーザーのフォロー
        unfollowed_element.follow_button_element = self.selenium.find_element(By.NAME, '100')
        unfollowed_element.follow_button_element.send_keys(Keys.ENTER)

        # フォローリストから削除するために再度アンフォロー
        # APIの通信が完了するまで待つ(フォロー済み)
        followed_element = wait.until(EC.presence_of_element_located((By.NAME, '100-follow')), message="")

        # ユーザーのアンフォロー
        followed_element.follow_button_element = self.selenium.find_element(By.NAME, '100')
        followed_element.follow_button_element.send_keys(Keys.ENTER)

        # フォローリストページを再読み込み
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:followings')))

        # フォローリストにユーザがいないことを確認
        self.selenium.find_element(By.NAME, 'user-none')

    def test_4(self):
        """地図機能を検証する"""

        # 地図処理の待ち時間
        wait = WebDriverWait(self.selenium, 10)

        # 地図ページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:map')))

        # ページタイトルの検証
        self.assertEquals('にゃっぷ | にゃっぷ', self.selenium.title)

        # APIの通信が完了するまで待つ
        mapelement = wait.until(EC.presence_of_element_located((By.NAME, 'diary_d')), message="")

        # 日記を見るボタンをクリック
        mapelement.diary_button_element = self.selenium.find_element(By.NAME, 'diary_d')
        mapelement.diary_button_element.send_keys(Keys.ENTER)

        # ページタイトルの検証
        self.assertEquals('日記詳細 | にゃっぷ', self.selenium.title)

        # トップページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('diary:diary')))
        self.selenium.maximize_window()

        # ページタイトルの検証
        self.assertEquals('トップページ ｜ にゃっぷ', self.selenium.title)

        # APIの通信が完了するまで待つ
        # 日記を見るボタンをクリック
        mapelement.diary_button_element = self.selenium.find_element(By.NAME, 'diary_d')
        mapelement.diary_button_element.send_keys(Keys.ENTER)

        # ページタイトルの検証
        self.assertEquals('日記詳細 | にゃっぷ', self.selenium.title)

