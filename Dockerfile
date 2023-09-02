FROM python:3.9-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1

ENV \
  PYTHONUNBUFFERED 1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apk add --no-cache netcat-openbsd

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head ; uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-level ${APP_LOGLEVEL:-info} --use-colors"]
