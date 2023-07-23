import datetime

from typing import Annotated, List
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import DateTime, ForeignKey

from core.models import Base


str50 = Annotated[str, 50]
intpk = Annotated[int, mapped_column(primary_key=True)]


class City(Base):
    """Город"""

    name: Mapped[str50]
    country: Mapped[str50]
    weathers: Mapped[List['Weather']] = relationship(back_populates='city')


class Weather(Base):
    """Погода"""

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    temp: Mapped[float]
    time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    city: Mapped['City'] = relationship(back_populates='weathers')
