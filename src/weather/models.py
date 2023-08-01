from datetime import datetime
from typing import Annotated, List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base


str50 = Annotated[str, 50]


class City(Base):
    """Город"""

    name: Mapped[str50]
    country: Mapped[str50]
    weathers: Mapped[List['Weather']] = relationship(back_populates='city')


class Weather(Base):
    """Погода"""

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    temp: Mapped[str]
    time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    city: Mapped['City'] = relationship(back_populates='weathers')
