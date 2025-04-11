# Python 3.10 の公式 slim イメージを使用
FROM python:3.10.13-slim-bullseye

# 作業ディレクトリを /app に設定
WORKDIR /app

# カレントディレクトリのファイルをコンテナにコピー
COPY ./ ./

# 必要なパッケージのインストールとPoetryセットアップ
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y wget curl build-essential \
  && pip install -U pip \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry run pip install -U pip setuptools \
  && poetry install \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# 環境変数の設定
ENV PYTHONPATH=/app
ENV LANG=ja_JP.UTF-8

# 起動コマンド
CMD ["./start.sh"]
