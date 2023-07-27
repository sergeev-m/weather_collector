#!/bin/sh

if [[ "${1}" == "celery" ]]; then
  celery --app=src.tasks.tasks:celery_app worker -l INFO

elif [[ "${1}" == 'beat' ]]; then
  celery --app=src.tasks.tasks:celery_app beat -l INFO

elif [[ "${1}" == "flower" ]]; then
  celery --app=src.tasks.tasks:celery_app flower

elif [[ "${1}" == "app" ]]; then
  alembic upgrade head &&
  gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
fi
