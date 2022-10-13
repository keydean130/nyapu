from .settings_common import *

# デバッグを有効にするか
DEBUG = False

# 許可するホストリスト
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

# ファイルの配置場所
STATICFILES_DIRS = (
os.path.join(BASE_DIR, "static"),
)

# 静的ファイルの配置場所
STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

# Amazon SES
AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

# ロギング設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'diary': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラの設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',  # ログローテーション（新しいファイルへの切り替え）間隔の単位（D＝日）
            'interval': 1,  # ログローテーション間隔（1日単位）
            'backupCount': 7,  # 保存しておくログファイル数
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(massage)s'
            ])
        },
    }
}

# セキュリティ関連設定

# security.W004
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# security.W012
SESSION_COOKIE_SECURE = True

# security.W016
CSRF_COOKIE_SECURE = True

# security.W021
# SECURE_HSTS_PRELOAD = True

# 末尾にスラッシュがないURLはリダイレクトしない
APPEND_SLASH = False

# サインアップにメールアドレス確認をはさむように設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

