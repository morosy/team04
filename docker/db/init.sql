CREATE DATABASE IF NOT EXISTS django_db;

CREATE USER IF NOT EXISTS 'team04'@'%' IDENTIFIED BY 'advinfteam04';

GRANT ALL PRIVILEGES ON django_db.* TO 'team04'@'%';

FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS user_info;
GRANT ALL PRIVILEGES ON user_info.* TO 'team04'@'%'; -- ★この行を追加
FLUSH PRIVILEGES; -- ★この行も追加 (権限変更をすぐに反映させるため)

USE user_info;

CREATE TABLE IF NOT EXISTS users (
    user_ID INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(10) NOT NULL,
    password VARCHAR(16) NOT NULL,
    current_coin INT DEFAULT 0,
    login_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    login_count INT DEFAULT 0
);

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
