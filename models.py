from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, String, Integer
Base = declarative_base()


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    color = Column(String)
    mileage = Column(String)
    location = Column(String)
    code = Column(String)
    url = Column(String)
    image = Column(String)
    time = Column(String)
    price = Column(String)


