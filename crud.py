from sqlalchemy.orm import Session
import schemas
from models import City, Sight


# CRUD для городов
def get_cities(db: Session):
    """
    Перечисление всех городов
    """
    return db.query(City).all()

def get_city(db: Session, city_id: int):
    """
    Вывод города по id
    """
    return db.query(City).filter_by(id=city_id).first()

def create_city(db: Session, schema: schemas.CityCreate):
    """
    Создать город
    """
    db_city = City(**schema.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, city_id: int, city_data: schemas.CityUpdate | dict):
    """
    Обновить город
    """
    db_city = db.query(City).filter_by(id=city_id).first()

    city_data = city_data if isinstance(city_data, dict) else city_data.model_dump()

    if db_city:
        for key, value in city_data.items():
            if hasattr(db_city, key):
                setattr(db_city, key, value)

        db.commit()
        db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    """
    Удалить город
    """
    db_city = db.query(City).filter_by(id=city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    return False


# CRUD для достопримечательностей
def get_sights(db: Session):
    """
    Перечисление всех достопримечательностей
    """
    return db.query(Sight).all()


def get_sight(db: Session, sight_id: int):
    """
    Вывод достопримечательности по ее id
    """
    return db.query(Sight).filter_by(id=sight_id).first()

def create_sight(db: Session, schema: schemas.SightCreate):
    """
    Создать достопримечательность
    """
    db_sight = Sight(**schema.model_dump())
    db.add(db_sight)
    db.commit()
    db.refresh(db_sight)
    return db_sight

def update_sight(db: Session, sight_id: int, sight_data: schemas.SightUpdate | dict):
    """
    Обновить достопримечательность
    """
    db_sight = db.query(Sight).filter_by(id=sight_id).first()

    sight_data = sight_data if isinstance(sight_data, dict) else sight_data.model_dump()

    if db_sight:
        for key, value in sight_data.items():
            if hasattr(db_sight, key):
                setattr(db_sight, key, value)

        db.commit()
        db.refresh(db_sight)
        return db_sight
    return None


def delete_sight(db: Session, sight_id: int):
    """
    Удалить достопримечательность
    """
    db_sight = db.query(Sight).filter_by(id=sight_id).first()
    if db_sight:
        db.delete(db_sight)
        db.commit()
        return True
    return False
