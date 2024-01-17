from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field, ValidationError
from typing import Union

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Ank4kanter@localhost:3306/locations'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = orm.declarative_base()


class ValidLoc(BaseModel):
    title: str = Field(min_length=3)
    url: str = Field(min_length=12)
    comment: Union[str, None] = Field(default=None, min_length=3)
    prio: int = Field(gt=0, lt=11)

# För testning
# loc = ValidLoc(title='anders', url='https://webbsallad.se', prio=7)

