from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CitySchema(BaseModel):
    model_config = ConfigDict(str_min_length=3, from_attributes=True)

    name: str
    country: str


class CityList(BaseModel):
    cities: list[CitySchema]


class WeatherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city_id: int
    temp: str
    time: datetime = datetime.utcnow()
    city: CitySchema
