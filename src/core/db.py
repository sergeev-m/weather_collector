import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.conf import settings
from core.models import Base
from log import log


def create_engine_and_session(url: str):
    try:
        engine = create_engine(url, future=True, echo=settings.DB_ECHO)
        log.info('Подключение к базе данных выполнено успешно')
    except Exception as e:
        log.error('❌ Ошибка подключения к базе данных', e)
        sys.exit()
    else:
        db_session = sessionmaker(bind=engine, autoflush=False)
        return engine, db_session


engine, db_session = create_engine_and_session(settings.database_url)


def get_db() -> Session:
    db = db_session()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
