#!/bin/bash

set -e

/wait-for-it.sh db:3306 --timeout=30 --strict -- echo "Database is up"

# Django の起動
python backend/manage.py runserver 0.0.0.0:8000 &

# Node アプリの起動（必要なら）
# cd frontend
# npm start

# wait によってバックグラウンドプロセスを維持
wait
