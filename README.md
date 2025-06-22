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


#### 変更履歴
<details>
<summary>
変更履歴
</summary>
- 2025/06/10 初期バージョン

- 2025/06/11 dockerfile関連記述追加

- 2025/06/19 内容全削除

- 2025/06/23 内容の全更新 簡単なgitコマンドの記述
</details>