# Pythonベースイメージ
FROM python:3.12-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの作成
WORKDIR /app

# 依存ファイルをコピー
COPY ./docker/web/requirements.txt /app/requirements.txt

# Pythonパッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

