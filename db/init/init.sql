-- データベース作成（既に存在しなければ）
CREATE DATABASE IF NOT EXISTS horse_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE horse_db;

-- テーブル作成（Djangoの models.py に対応）
CREATE TABLE IF NOT EXISTS core_horse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10),
    trainer VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 初期データを挿入
INSERT INTO core_horse (name, birth_date, gender, trainer) VALUES
('サクラチヨノオー', '1990-03-01', '牡', '田中調教師'),
('マヤノトップガン', '1993-04-19', '牡', '佐藤調教師'),
('ウオッカ', '2004-04-04', '牝', '藤原調教師');
