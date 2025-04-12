#! /usr/bin/env sh
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOGCONFIG=${LOGCONFIG:-"./logging.conf"}
WORKERS=${WORKERS:-1}
APP_MODULE=${APP_MODULE:-"main:app"}

exec poetry run uvicorn \
  --reload \
  --host $HOST \
  --port $PORT \
  --log-level $LOG_LEVEL \
  --log-config $LOGCONFIG \
  --workers $WORKERS \
  "$APP_MODULE"