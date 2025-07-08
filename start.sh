#!/bin/bash

set -e

/wait-for-it.sh db:3306 --timeout=30 --strict -- echo "Database is up"

echo "=== DB初期化スクリプトを実行中 ==="
cd /app/docker/init
python init.py
echo "=== 初期化完了 ==="

echo "=== Django マイグレーション実行 ==="
python /app/backend/manage.py migrate

echo "=== Django 開始 ==="
exec python /app/backend/manage.py runserver 0.0.0.0:8000
