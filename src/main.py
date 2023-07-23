from core.conf import settings
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from core.db import create_db_and_tables, get_db, db_session
from weather.models import Weather
from weather.schemas import WeatherSchema
from weather.services import get_cities
from tasks.tasks import collect_weather
from tasks.tasks import celery_app
from weather.services import get_weather


app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    version=settings.VERSION
)


@app.get("/", response_model=list[WeatherSchema])
def root(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Weather)[skip: limit + skip]


@app.on_event("startup")
def on_startup() -> None:
    with db_session() as db:
        create_db_and_tables()
        get_cities(db)
        get_weather(db)


@app.on_event('shutdown')
def shutdown_task() -> None:
    celery_app.control.revoke(collect_weather.request.id, terminate=True)
