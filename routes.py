from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (get_cities, get_city, create_city, update_city, delete_city,
                  get_sights, get_sight, create_sight, update_sight, delete_sight)

router_websocket = APIRouter()
router_cities = APIRouter(prefix='/cities', tags=['Города'])
router_sights = APIRouter(prefix='/sights', tags=['Достопримечательности'])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{userId}")
async def websocket_endpoint(websocket: WebSocket, userId: int):
    """
    Системные сообщения, вход и выход пользователя
    """
    await manager.connect(websocket)
    await manager.broadcast(f"User{userId} присоединился")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User{userId}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User{userId} покинул чат")

# Города
@router_cities.get("/", response_model=List[schemas.City])
async def read_cities(db: Session = Depends(get_db)):
    """
    Вывод всех городов
    """
    cities = get_cities(db)
    return cities


@router_cities.get("/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: Session = Depends(get_db)):
    """
    Вывод города по id
    """
    city = get_city(db, city_id)
    return city

@router_cities.post("/", response_model=schemas.City)
async def create_city_route(city_data: schemas.CityCreate, db: Session = Depends(get_db)):
    """
    Создать город
    """
    city = create_city(db, city_data)
    await notify_clients(f"Город добавлен: {city.name}")
    return city

@router_cities.patch("/{city_id}", response_model=schemas.City)
async def update_city_route(city_id: int, city_data: schemas.CityUpdate, db: Session = Depends(get_db)):
    """
    Изменить город
    """
    updated_city = update_city(db, city_id,city_data)
    if updated_city:
        await notify_clients(f"Город {updated_city.name} обновлен")
        return updated_city
    return {"message": "Город не найден"}


@router_cities.delete("/{city_id}")
async def delete_city_route(city_id: int, db: Session = Depends(get_db)):
    """
    Удалить город
    """
    deleted = delete_city(db, city_id)
    if deleted:
        await notify_clients(f"Город с id {city_id} удален")
        return {"message": "Город удален"}
    return {"message": "Город не найден"}


# Достопримечательности
@router_sights.get("/", response_model=List[schemas.Sight])
async def read_sights(db: Session = Depends(get_db)):
    """
    Вывести все достопримечательности
    """
    sights = get_sights(db)
    return sights


@router_sights.get("/{sight_id}", response_model=schemas.Sight)
async def read_sight(sight_id: int, db: Session = Depends(get_db)):
    """
    Вывести достопримечательность по id
    """
    sight = get_sight(db, sight_id)
    return sight

@router_sights.post("/", response_model=schemas.Sight)
async def create_sight_route(schema: schemas.SightCreate, db: Session = Depends(get_db)):
    """
    Создать достопримечательность
    """
    sight = create_sight(db, schema)
    await notify_clients(f"Достопримечательность создана: {sight.name}")
    return sight

@router_sights.patch("/{sight_id}")
async def update_sight_route(sight_id: int, schema: schemas.SightUpdate, db: Session = Depends(get_db)):
    """
    Обновить достопримечательность
    """
    updated_sight = update_sight(db, sight_id, schema)
    if updated_sight:
        await notify_clients(f"Достопримечательность {updated_sight.name} обновлена")
        return updated_sight
    return {"message": "Достопримечательность не найдена"}


@router_sights.delete("/{sight_id}")
async def delete_sight_route(sight_id: int, db: Session = Depends(get_db)):
    """
    Удалить достопримечательность
    """
    deleted = delete_sight(db, sight_id)
    if deleted:
        await notify_clients(f"Достопримечательность с id {sight_id} удалена")
        return {"message": "Достопримечательность удалена"}
    return {"message": "Достопримечательность не найдена"}
