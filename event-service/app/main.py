from fastapi import FastAPI
from app.api.v1.events import router as events_router


def create_app():
    app = FastAPI(title="Event Service")

    app.include_router(events_router, prefix="/api/v1/events", tags=["Events"])

    return app


app = create_app()
