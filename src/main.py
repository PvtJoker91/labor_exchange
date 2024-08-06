from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container
from api import router as api_router
import uvicorn

from di import AppProvider
from core.config import settings, Settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router=api_router)

    return app


def create_production_app():
    app = create_app()
    container = make_async_container(AppProvider(), context={Settings: settings})
    setup_dishka(container, app)
    return app


if __name__ == '__main__':
    uvicorn.run("main:create_app", port=8000, reload=True)
