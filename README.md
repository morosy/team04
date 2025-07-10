## git コマンド

#### 作業開始時
> [!WARNING]
> 作業開始前に必ず実行
```
git checkout main
git pull origin main
```
または
```
git fetch origin
git merge origin/main  # または git rebase origin/main
```

新しく作業ブランチを作成
```
git checkout -b [ブランチ名]
```

または既存ブランチに入る
```
git checkout [ブランチ名]
```


#### 作業完了後

> [!WARNING]
> 競合を防ぐために最新のリモートリポジトリを取得
```

git checkout main
git pull origin main
git checkout [ブランチ名]
```
または
```
git fetch origin
git merge origin/main  # または git rebase origin/main
```

push
```
git add .
git commit -m "[コミットメッセージ]"
git push origin [ブランチ名]
```

ブランチのプッシュが初めての場合は以下を利用
```
git push -u origin [ブランチ名]
```


#### 必要であれば作業終了後にmainに戻る
```
git checkout main
```


#### Github 操作
> [!IMPORTANT]
> 変更が他ファイルや環境に依存する場合や大規模な場合は必ず対象者にレビューを依頼する


## Docker コマンド
#### コンテナのビルド，起動
```
docker-compose up -d --build
```

#### Djangoのトップページリンク
```
http://localhost:8000/
```

#### Dockerへの入り方
```
docker exec -it <コンテナ名> /bin/bash
```

## Docker上のデータベース確認手順
```
# MySQLへ入る
docker-compose exec db mysql -u team04 -p

# データベース一覧表示
SHOW DATABASES;

# 操作するデータベースを選択
USE [DATABASE_NAME];

# テーブル一覧の表示
SHOW TABLES;

# テーブルカラムの表示
DESCRIBE users;

# テーブルの内容表示
SELECT * FROM [TABLE_NAME];
```

## 起動手順(デバッグアカウント作成含む)
```
# Dockerコンテナのビルドと起動
docker-compose up -d --build

# Dockerコンテナに入る
docker-compose exec web /bin/bash

# テストアカウントの作成
cd docker/init
python init.py

# Webブラウザで以下にアクセス
http://localhost:8000/

# 作成したアカウントでログイン(例)
ID: 00000001
PASSWORD: password1
```

## 総合テスト用 起動手順

> [!WARNING]
> 絶対パスに日本語や全角文字，スペースなどが含まれないディレクトリにて作業を開始して下さい


#### リポジトリのクローン
`git clone https://github.com/morosy/team04.git`

#### Dockerコンテナのビルド、起動
`docker-compose up -d --build`


以下のような表示があれば基本的に成功
```
 ✔ Service web              Built                                                                                                   2.5s 
 ✔ Network team04_default   Created                                                                                                 0.0s 
 ✔ Volume "team04_db_data"  Created                                                                                                 0.0s 
 ✔ Container team04-db-1    Started                                                                                                 0.1s 
 ✔ Container team04-web-1   Started 
```

#### 初期データの挿入
Dockerコンテナに入る
`docker-compose exec web /bin/bash`

初期データ挿入用スクリプトの実行
`cd docker/init`
`python init.py`

> [!IMPORTANT]
> `python docker/init/init.py`というようにディレクトリ移動を省くとファイル参照ができなくなり，実行が失敗する


以下のような表示があれば成功
```
=== 待機中 ===
=== ユーザー挿入中 ===
User 'testuser1' inserted with ID 1
User 'testuser2' inserted with ID 2
User 'testuser3' inserted with ID 3
User 'testuser4' inserted with ID 4
User 'testuser5' inserted with ID 5
=== 挿入完了 ===
=== 待機中 ===
=== ユーザー結果挿入中 ===
user_ID=1 に 10 件のデータを挿入しました。
user_ID=2 に 50 件のデータを挿入しました。
user_ID=3 に 20 件のデータを挿入しました。
user_ID=4 に 10 件のデータを挿入しました。
```


#### Webブラウザでアクセス
`http://localhost:8000/`

#### 以下のいずれかのアカウントでログイン
```
# team04
ID: 00000001
PASSWORD: advinfteam04

# testuser2
ID: 00000002
PASSWORD: password2

# testuser3
ID: 00000003
PASSWORD: password3

# testuser4
ID: 00000004
PASSWORD: password4

# testuser5
ID: 00000005
PASSWORD: password5
```

#### MySQLの操作
```
# データベースにアクセス
# コンテナ外からコマンド入力
docker-compose exec db mysql -u team04 -p

# passwordの入力
password: advinfteam04

# データベース一覧表示
SHOW DATABASES;

# 操作するデータベースを選択
USE [DATABASE_NAME];

# テーブル一覧の表示
SHOW TABLES;

# テーブルカラムの表示
DESCRIBE [TABLE_NAME];

# テーブルの内容表示
SELECT * FROM [TABLE_NAME];
```

#### MySQLからの脱出
`exit`


#### コンテナからの脱出方法
`exit`

#### コンテナのシャットダウン・削除
`docker-compose down -v`


#### 変更履歴
<details>
<summary>
変更履歴
</summary>

- 2025/06/10 初期バージョン
- 2025/06/11 dockerfile関連記述追加
- 2025/06/19 内容全削除
- 2025/06/23 内容の全更新 簡単なgitコマンドの記述
- 2025/06/29 Docker コマンドの追加
- 2025/07/03 MySQL用コマンドの追加
- 2025/07/03 デバッグ開始の記述追加
- 2025/07/04 記述の整理
- 2025/07/04 総合テスト用記述の追加
</details>