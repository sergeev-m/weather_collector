from datetime import datetime

from pydantic import BaseModel


class CitySchema(BaseModel):
    name: str
    country: str

    class Config:
        from_attributes = True


class WeatherSchema(BaseModel):
    city_id: int
    temp: float
    time: datetime = datetime.now()
    city: CitySchema
