from sqlalchemy import Boolean, Column, Integer, String, Text
from database import Base


class Locations(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), primary_key=False, index=True)
    url = Column(String(100))
    comment = Column(Text)
    prio = Column(Integer)
