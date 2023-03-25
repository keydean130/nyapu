# にゃっぷ紹介 <img src="https://user-images.githubusercontent.com/112099340/188294475-50ddd4cf-69bf-4c5b-820f-2618ad8f8345.png" width="25px">

## (現在は本番環境停止中)

## １、アプリ概要
にゃっぷは位置情報を利用した、猫専用の日記投稿アプリです。  
身近な場所にいる、可愛い猫たちを見つけられます。  
<img src="https://user-images.githubusercontent.com/112099340/188298226-050b5e46-1af1-4707-84ef-386621fd21ba.gif" width="750px">|


## ２、制作意図
猫好きの方が猫のみ楽しんでもらえるSNSを作りたいという思いから作成しました。  
身近にいる猫たちを知ってもらうことで、野良猫の保護などにも繋がると思いました。  


## ３、制作期間と担当範囲
制作期間は約半年。書籍「動かして学ぶ！Python Django開発入門」の日記投稿アプリをベースにして、  
機能追加（いいね機能・コメント機能・検索機能・地図機能・猫の品種分類機能・おすすめ機能）、デザイン変更を行いました。  


## ４、機能紹介
にゃっぷで利用可能な機能の一覧です。
使い方は各リンクに記載しています。
### ■ ユーザーの機能  
- [ユーザーの登録](https://github.com/keydean130/nyapu/issues/4)  
- [ユーザーのプロフィール作成](https://github.com/keydean130/nyapu/issues/11)  
- [ユーザーのフォロー機能](https://github.com/keydean130/nyapu/issues/5)  

### ■ 日記共有機能
- [日記作成、更新、削除](https://github.com/keydean130/nyapu/issues/1)  
- [日記へのいいね機能](https://github.com/keydean130/nyapu/issues/2)  
- [日記へのコメント機能](https://github.com/keydean130/nyapu/issues/3)  

### ■ 検索機能
- [日記のキーワード検索](https://github.com/keydean130/nyapu/issues/6)  

### ■ 地図機能
- [地図上に日記の表示](https://github.com/keydean130/nyapu/issues/7)  

### ■ 問い合わせ機能
- [問い合わせフォーム](https://github.com/keydean130/nyapu/issues/8)  

### ■ 猫の品種分類機能
- Pytorchで学習データを作成し、実装

### ■ おすすめ機能
- 品種分類の結果や位置情報から、ユーザへのおすすめの日記を表示


## ５、工夫した箇所
直感的に使用できるよう、以下の2点を工夫しました。  
- 日記のいいね、ユーザーのフォロー・アンフォローなどは非同期通信を使用。  

- 日記に位置情報を紐づけて、地図上から日記の分布を確認可能。  

## ６、主な使用技術
- Python 3.7.10  
- Django 3.2.14
- Pytorch
- PostgreSQL 10.17
- AWS
  - VPC  
  - EC2
  - Route53
  - SES
- Nginx 1.12.2
- Gunicorn 19.10
- Docker 20.10.12/Docker-compose 1.25.0 (開発環境のみ)
- CircleCI 2.1

構成図は以下になります。
![にゃっぷインフラ構成図](https://user-images.githubusercontent.com/112099340/197382272-3506273b-293f-4d91-94f0-6edfd33203ae.png)
Githubにpushされると自動テストが実行されます。  
masterブランチにpushされ、自動テストが成功した場合のみ、EC2のAPサーバに自動デプロイされます。

## ７、DB設計
![image](https://user-images.githubusercontent.com/112099340/191403317-a630b4bc-dacf-48d9-8cd4-8a442a0c02e1.png)

## ８、テスト
- ユニットテスト
基本機能（ログイン、日記の作成・更新・削除、コメントの作成・削除）をユニットテストしています。

- UIテスト  
seleniumにてログイン機能・いいね機能・フォロー機能・地図機能をUIテストしています。


