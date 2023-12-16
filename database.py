from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext. declarative import declarative_base
from pydantic import BaseModel, field_validator, Field
import typing

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Ank4kanter@localhost:3306/locations'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Locations(BaseModel):
    title: str = Field(min_length=3)
    url: str = Field(min_length=12)
    # comment: typing.Optional[str] = Field(None, min_length=3)
    comment: str = Field(min_length=3)
    prio: int = Field(gt=0, lt=11)
