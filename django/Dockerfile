# 公式からイメージをpull
FROM python:3.9-buster

# コンテナの作業ディレクトリを設定
WORKDIR /usr/src/django

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

# aptで依存関係のインストール
RUN apt-get update && apt-get install -y unzip wget vim

# pipenvをインストール
RUN pip install --upgrade pip && \
    pip install pipenv

# ホストのdjangoディレクトリを、コンテナにコピー
COPY ./django /usr/src/django

# ホストのdistディレクトリを、コンテナにコピー
COPY ./dist /usr/src/dist

# pipfileからパッケージをインストール
RUN python -m pipenv install

# entrypoint.shを実行
ENTRYPOINT ["/usr/src/django/entrypoint.sh"]