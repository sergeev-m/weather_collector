import csv
import os
import requests

from typing import Any, Type, Union
from sqlalchemy import insert
from sqlalchemy.orm import Query, Session

from core.conf import CsvPath, settings
from log import log
from weather.models import City, Weather


def get_city_temp(city: str, country: str,
                  units: str = 'metric') -> Union[float, int]:
    params = {
        'q': f'{city},{country}',
        'appid': settings.API_KEY,
        'units': units
    }
    res = requests.get(settings.WEATHER_URL, params=params, timeout=3)
    res.raise_for_status()
    data = res.json()
    temp = data['main']['temp']
    return temp


def get_weather(db: Session) -> Union[Query[Type[Weather]], Query[Any]]:
    try:
        cities = db.query(City).all()
        data = [
            Weather(temp=get_city_temp(city.name, city.country), city=city)
            for city in cities
        ]
        db.add_all(data)
        db.commit()

    except requests.HTTPError as exc:
        log.error(exc)
    except Exception as exc:
        log.error(exc)
    queryset = db.query(Weather).order_by(Weather.time.desc())
    return queryset[:settings.NUMBER_OF_RESULT_CITIES]


def get_cities(db: Session) -> None:
    file_path = os.path.join(CsvPath, 'cities.csv')
    if db.query(City).first():
        return
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            data = list(csv.DictReader(csvfile, delimiter=','))
    except EOFError as exc:
        log.error(exc)
    except FileNotFoundError as exc:
        raise exc
    else:
        db.execute(insert(City), data)
        db.commit()
        log.info('Успешная загрузка городов в БД')
        return
