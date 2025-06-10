#### フォークしたリポジトリをローカルにクローン
```
git clone https://github.com/[username]/team04.git
cd team04
```

#### 上流(オリジナル)のリモートを追加
```
git remote add upstream https://github.com/morosy/team04.git
```

#### 最初の内容を追加
```
git fetch upstream
git checkout main
git merge upstream/main
```

#### ブランチを作成してチェックアウト
```
git checkout -b feature/[your-feature-name]
```

#### 編集 コミット
```
# 編集作業をしてから
git add .
git commit -m "[message]"
```


#### リポジトリにプッシュ
```
git push origin feature/[your-feature-name]
```


## Docker
```bash
> cd team04
> docker-compose up --build -d
 ✔ web Built
 ✔ Network team04_default   Created
 ✔ Volume "team04_db_data"  Created
 ✔ Container team04-db-1    Started
 ✔ Container team04-web-1   Started

> docker-compose logs web
time="2025-06-11T02:09:01+09:00" level=warning msg="D:\\dev\\team04\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
web-1  | wait-for-it.sh: waiting 15 seconds for db:3306
web-1  | wait-for-it.sh: db:3306 is available after 8 seconds
web-1  | Watching for file changes with StatReloader

# Docker 停止
> docker-compose down
time="2025-06-11T02:12:40+09:00" level=warning msg="D:\\dev\\team04\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[+] Running 3/3
 ✔ Container team04-web-1  Removed
 ✔ Container team04-db-1   Removed
 ✔ Network team04_default  Removed
```

[page](http://localhost:8000/)