## 質問
ストアドプロシージャについて、Pythonを用いて以下を発火させる方法を教えてください。
アクセス情報は以下のaccess.txtを利用します。
```
172.21.33.203
team04
team04
```


```
USE user_info;

DELIMITER $$

CREATE PROCEDURE create_user_result_table(IN uid INT, IN uname VARCHAR(10))
BEGIN
    -- テーブル名を user_result_[user_ID] にする
    SET @table_name = CONCAT('user_result_', uid);

    -- CREATE TABLE の動的SQL生成
    SET @sql = CONCAT(
        'CREATE TABLE IF NOT EXISTS ', @table_name, ' (',
        'user_ID INT NOT NULL, ',
        'date INT NOT NULL, ',
        'category INT NOT NULL, ',
        'result VARCHAR(20) NOT NULL, ',
        'change_coin INT NOT NULL, ',
        'current_coin INT NOT NULL, ',
        'PRIMARY KEY (user_ID, date, category)',
        ');'
    );

    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$

DELIMITER ;
```
```
USE friend;

DELIMITER $$

CREATE PROCEDURE create_friend_table(IN uid INT)
BEGIN
    SET @sql = CONCAT(
        'CREATE TABLE IF NOT EXISTS friend_user_', uid, ' (',
        'user_ID INT NOT NULL, ',
        'target_ID INT NOT NULL, ',
        'friend BOOLEAN DEFAULT FALSE, ',
        'receive_request BOOLEAN DEFAULT FALSE, ',
        'PRIMARY KEY (user_ID, target_ID)',
        ');'
    );
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$

DELIMITER ;
```


## 回答

Python で **MySQL のストアドプロシージャを呼び出して発火させるスクリプト** を作成する方法を示します。
以下のコードでは、`mysql-connector-python` を使って、`access.txt` の情報を読み込み、ストアドプロシージャを呼び出します。

---

### 1️⃣ 必要なモジュールをインストール（まだの場合）

```bash
pip install mysql-connector-python
```

---

### 2️⃣ `access.txt` の内容例（すでにお持ちのもの）

```
172.21.33.203
team04
team04
```

---

### 3️⃣ Python スクリプト例

```python
import mysql.connector

def read_access_info(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    host = lines[0]
    user = lines[1]
    password = lines[2]
    return host, user, password

def call_create_user_result_table(cursor, uid, uname):
    cursor.execute("USE user_info;")
    cursor.callproc("create_user_result_table", (uid, uname))

def call_create_friend_table(cursor, uid):
    cursor.execute("USE friend;")
    cursor.callproc("create_friend_table", (uid,))

def main():
    access_file = "access.txt"
    host, user, password = read_access_info(access_file)

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # 必要に応じてプロシージャを作成する（既に作成済みなら不要）
        # cursor.execute("USE user_info;")
        # cursor.execute("""CREATE PROCEDURE ...""")  # 事前に MySQL 側で作成しておくのが普通です

        # ストアドプロシージャの呼び出し
        call_create_user_result_table(cursor, 1, 'testuser')
        print("create_user_result_table 発火完了")

        call_create_friend_table(cursor, 1)
        print("create_friend_table 発火完了")

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
```

---

### 💡 注意点

✅ このスクリプトは次の前提です：

* ストアドプロシージャは **すでにデータベース上で作成済み**。
* ユーザー `team04` に必要な権限（ストアドプロシージャの実行権限、テーブル作成権限）がある。
* `access.txt` はスクリプトと同じディレクトリにある。

✅ ストアドプロシージャの作成も Python からやりたい場合は、SQL ファイルを読み込んで `cursor.execute()` で実行可能ですが、DELIMITER の扱いに注意が必要です。通常は MySQL クライアントやツールで事前に作成します。

---

### ⭐ もし「ストアドプロシージャの作成も Python でやりたい」という場合は、そのコード例も作成しますので教えてください！
