# 公式からpython3.9 busterイメージをpull
FROM python:3.9-buster

# 作業ディレクトリを設定
WORKDIR /usr/src/app

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

# ホストのpipfiletをコンテナの作業ディレクトリにコピー
COPY ./Pipfile /usr/src/app/Pipfile

# pipfileからパッケージをインストール
RUN python -m pipenv install --skip-lock

# entrypoint.shをコピー
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# ホストのカレントディレクトリ（現在はappディレクトリ）を作業ディレクトリにコピー
COPY . /usr/src/app

# entrypoint.shを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]