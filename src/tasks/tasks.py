from log import log
from core.db import db_session
from weather.services import get_weather
from celery import Celery

from core.conf import settings


celery_app = Celery(settings.CELERY_TASK_NAME, broker=settings.redis_url)


@celery_app.task(name='collect_weather')
def collect_weather():
    with db_session() as db:
        try:
            get_weather(db)
            log.info('OK')
        except Exception as exc:
            log.error(exc)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    celery_app.add_periodic_task(
        settings.TEMP_UPDATE_INTERVAL, collect_weather.s(), name='every_hour'
    )


celery_app.conf.timezone = 'UTC'
celery_app.conf.update(
    task_track_started=True,
    task_time_limit=600,
)