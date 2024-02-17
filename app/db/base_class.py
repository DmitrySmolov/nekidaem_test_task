from datetime import datetime

from inflect import engine
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base, declared_attr


class Prebase:

    @declared_attr
    def __tablename__(cls) -> str:
        singular_name = cls.__name__.lower()
        plural_name = engine().plural(singular_name)
        return plural_name

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base = declarative_base(cls=Prebase)
