from fastapi import FastAPI

from helpers.app_helper import startup_event, shutdown_event
from routers import (
    health,
)


def init_routers(app_):
    for router in (health,):
        app_.include_router(router.router, prefix="/api/v1")


def create_app():
    app_ = FastAPI(
        title="QuizAPI",
        description="Quiz API",
        version="1.0.0",
        on_startup=[startup_event],
        on_shutdown=[shutdown_event],
    )
    init_routers(app_)
    return app_


app = create_app()
