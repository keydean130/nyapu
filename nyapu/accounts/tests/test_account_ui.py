from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLogin(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()     
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox') 
        options.add_argument('--headless') 
        options.add_argument('--disable-gpu')
        cls.selenium = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=options, )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://nyapu:8000' + str(reverse_lazy('account_login')))
        # ログイン
        email_input = self.selenium.find_element(By.NAME, "login")
        email_input.send_keys('testonly@example.com')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('onlynyapu')
        self.selenium.find_element(By.NAME, "btn").click()
        # ページタイトルの検証
        self.assertEquals('トップページ ｜ にゃっぷ', self.selenium.title)
