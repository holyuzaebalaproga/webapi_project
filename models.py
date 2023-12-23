from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# класс города
class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    sights = relationship('Sight', back_populates='city')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())

# класс достопримечательности
class Sight(Base):
    __tablename__ = 'sights'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', back_populates='sights')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())