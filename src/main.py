from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container
from api import router as api_router
import uvicorn

from containers.providers import AppProvider
from core.config import settings, Settings

container = make_async_container(AppProvider(), context={Settings: settings})


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router=api_router)
    setup_dishka(container, app)

    return app


if __name__ == '__main__':
    uvicorn.run("main:create_app", port=8000, reload=True)
