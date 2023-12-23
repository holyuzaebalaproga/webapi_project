from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# city
class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Optional[str] = None


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


# Sight
class SightBase(BaseModel):
    name: str
    description: str
    city_id: int


class SightCreate(SightBase):
    pass


class SightUpdate(SightBase):
    name: Optional[str] = None
    city_id: Optional[int] = None


class Sight(SightBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
