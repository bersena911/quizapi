from fastapi import FastAPI

from helpers.app_helper import shutdown_event
from routers import (
    health_router,
    auth_router,
    quiz_router,
    question_router,
    game_router,
)


def init_routers(app_):
    for router in (
        health_router,
        auth_router,
        quiz_router,
        question_router,
        game_router,
    ):
        app_.include_router(router.router, prefix="/api/v1")


def create_app():
    app_ = FastAPI(
        title="QuizAPI",
        description="Quiz API",
        version="1.0.0",
        on_shutdown=[shutdown_event],
    )
    init_routers(app_)
    return app_


app = create_app()
