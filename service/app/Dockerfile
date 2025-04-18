# Python 3.10 の公式 slim イメージを使用
FROM python:3.10.13-slim-bullseye

# 作業ディレクトリを /app に設定（app ディレクトリの中がプロジェクトルート）
WORKDIR /app

# 必要なパッケージと Poetry のインストール
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y wget curl build-essential \
  && pip install -U pip \
  && pip install motor \
  && pip install poetry \
  && pip install PyJWT \
  && poetry config virtualenvs.create false \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# プロジェクトフォルダだけをコピー（ホストの ./app → コンテナの /app）
COPY . /app

# Poetry の依存関係インストール
RUN poetry install --no-root

# 環境変数の設定
ENV PYTHONPATH=/app
ENV LANG=ja_JP.UTF-8

# 実行コマンド（start.sh は app ディレクトリ内にある前提）
CMD ["./start.sh"]
