#!/bin/sh

if [[ "$1" == "celery" ]]; then
  celery --app=src.tasks.tasks:celery_app worker -l INFO
elif [[ "$1" == 'beat' ]]; then
  celery --app=src.tasks.tasks:celery_app beat -l INFO
elif [[ "$1" == "flower" ]]; then
  celery --app=src.tasks.tasks:celery_app flower
elif [[ "$1" == "app" ]]; then
  alembic upgrade head &&
#  gunicorn src.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
else
  echo "Unknown or missing sub-command: '$1'"
  usage
  exit 1
fi
