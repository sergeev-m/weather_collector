from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, comment='primary_key'
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __str__(self):
        return '%s(id=%s)' % (type(self).__name__, self.id)

    def __repr__(self) -> str:
        return str(self)
