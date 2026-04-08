from fastapi import FastAPI

from app.api.routes import detect, feedback, frontend, health, messages, stats
from app.db.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="ScamShield AI", version="0.1.0")

    Base.metadata.create_all(bind=engine)

    app.include_router(frontend.router)
    app.include_router(health.router, tags=["health"])
    app.include_router(detect.router, tags=["detect"])
    app.include_router(feedback.router, tags=["feedback"])
    app.include_router(messages.router, tags=["messages"])
    app.include_router(stats.router, tags=["stats"])
    return app


app = create_app()
