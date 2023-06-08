# 公式からイメージをpull
FROM node:18.13.0

# コンテナの作業ディレクトリを設定
WORKDIR /usr/src/vue

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y rsync

# ホストのvueディレクトリを、コンテナにコピー
COPY ./vue /usr/src/vue

# ホストのdistディレクトリを、コンテナにコピー
COPY ./dist /usr/src/dist

# パッケージマネージャーを設定
RUN npm install -g npm@8.19.3

# アプリケーションの依存関係をインストール
RUN npm install axios vuetify@3

# ビルドコマンドを実行（必要に応じて変更）
RUN npm run build

# コンテナが起動した時に実行されるコマンドを指定（必要に応じて変更）
# CMD [ "npm", "run", "start" ]