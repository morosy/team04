FROM python:3.12-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


COPY wait-for-it.sh /wait-for-it.sh
COPY start.sh /start.sh
# 相対パス
COPY ../../start.sh /start.sh
COPY ../../wait-for-it.sh /wait-for-it.sh

RUN chmod +x /wait-for-it.sh /start.sh
