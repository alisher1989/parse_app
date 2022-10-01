from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from database import Base


class Record(Base):
    __tablename__ = "Records"

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(500), index=True)
    price = Column(String)
    date = Column(String)
