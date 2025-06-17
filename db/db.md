#### 各ユーザの過去データ
ストアドプロシージャの作成
```
USE user_info;
```

ストアドプロシージャの作成
ここをコピー
```
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

#### フレンドデータベース

フレンドデータベースの追加
```
CREATE DATABASE IF NOT EXISTS friend;
```

ストアドプロシージャの作成
ここをコピー
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