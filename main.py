from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import models
from database import engine
from routes import router_websocket, router_cities, router_sights

# создание приложения на FastAPI
app = FastAPI(title="The tourist's book",
              summary="Приложение для добавления и обсуждения популярных и секретных достопримечательностей в городах мира ✈️",
              description="Рассохина Анастасия Дмитриевна, РИ-310936",
              contact={
                "name": "Главная страница",
                "url": "http://localhost:8000/"
              },
)

# создание таблиц
models.Base.metadata.create_all(bind=engine)

# создание шаблона jinja
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, tags=["Проверка"])
async def read_root(request: Request):
    """
    HTML главной страницы
    """
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})

@app.get("/ip", tags=["Проверка"])
async def read_root(request: Request):
    """
    Вывод ip пользователя
    """
    return request.client.host

# подключение роутеры в приложение
app.include_router(router_websocket)
app.include_router(router_cities)
app.include_router(router_sights)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
