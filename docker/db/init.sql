/*
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/11 Version: 1.0
    change: 2025/06/23 Version: 1.1
          : 2025/07/01 Version: 1.2
        init.sqlの内容を完全化・本番環境に従う内容
    Description: ホーム画面のhtmlファイル
    Note: このファイルは, Dockerコンテナ内のMySQLに初期データを投入するためのSQLスクリプトです。
    Usage: このファイルは、Dockerコンテナの初期化時に実行されるように設定する。
        基本的な使い方は以下のとおり
        mysql -h [IP Address] -u [username] -p < init.sql
*/


-- ユーザーと権限
CREATE USER IF NOT EXISTS 'team04'@'%' IDENTIFIED BY 'team04';
GRANT ALL PRIVILEGES ON *.* TO 'team04'@'%';
FLUSH PRIVILEGES;

-- ============================
-- user_info データベースとテーブル
-- ============================
CREATE DATABASE IF NOT EXISTS user_info;
GRANT ALL PRIVILEGES ON user_info.* TO 'team04'@'%';
FLUSH PRIVILEGES;

USE user_info;

CREATE TABLE IF NOT EXISTS users (
    user_ID INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(10) NOT NULL,
    password VARCHAR(16) NOT NULL,
    current_coin INT DEFAULT 0,
    login_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    login_count INT DEFAULT 0,

    -- 勝ち数および負け数のカラムを追加
    number_of_wins INT DEFAULT 0,
    number_of_losses INT DEFAULT 0
);

-- ストアドプロシージャ: create_user_result_table
DELIMITER $$

CREATE PROCEDURE create_user_result_table(IN uid INT, IN uname VARCHAR(10))
BEGIN
    SET @table_name = CONCAT('user_result_', uid);

    SET @sql = CONCAT(
        'CREATE TABLE IF NOT EXISTS ', @table_name, ' (',
        'user_ID INT NOT NULL, ',
        'date BIGINT NOT NULL, ',
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

-- ============================
-- horse_data データベースとテーブル
-- ============================
CREATE DATABASE IF NOT EXISTS horse_data;
USE horse_data;

CREATE TABLE IF NOT EXISTS horse_status (
    id INT PRIMARY KEY AUTO_INCREMENT,
    body_weight INT NOT NULL,
    power INT NOT NULL,
    speed INT NOT NULL,
    stamina INT NOT NULL,
    clear_weather_status INT NOT NULL,
    light_rain_status INT NOT NULL,
    heavy_rain_status INT NOT NULL,
    grass_status INT NOT NULL,
    dirt_status INT NOT NULL,
    sprint_status INT NOT NULL,
    middle_status INT NOT NULL,
    long_status INT NOT NULL
);

-- ============================
-- friend データベースとストアドプロシージャ
-- ============================
CREATE DATABASE IF NOT EXISTS friend;
USE friend;

CREATE TABLE IF NOT EXISTS friend_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_user_id INT NOT NULL,     -- 申請したユーザー
    to_user_id INT NOT NULL,       -- 申請を受けたユーザー
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    request_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS friends (
    user_id INT NOT NULL,
    friend_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id) REFERENCES user_info.users(user_ID),
    FOREIGN KEY (friend_id) REFERENCES user_info.users(user_ID)
);

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
