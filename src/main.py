from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.core.conf import settings
from src.core.db import db_session, get_db
from src.tasks.tasks import celery_app, collect_weather
from src.weather.models import Weather
from src.weather.schemas import WeatherSchema
from src.weather.services import get_cities, get_weather


app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    version=settings.VERSION
)


@app.get("/", response_model=list[WeatherSchema])
def weather(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Weather)[skip: limit + skip]


@app.on_event("startup")
def on_startup() -> None:
    with db_session() as db:
        get_cities(db)
        get_weather(db)


@app.on_event('shutdown')
def shutdown_task() -> None:
    celery_app.control.revoke(collect_weather.request.id, terminate=True)
