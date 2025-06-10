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