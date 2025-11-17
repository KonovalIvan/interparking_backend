from fastapi import FastAPI
from app.api.v1.events import router as events_router


def create_app():
    app = FastAPI(title="Event Service",
                  docs_url=None,
                  redoc_url=None,
                  )

    app.include_router(events_router, prefix="/api/v1/events", tags=["Events"])

    return app

# TODO: change dir in dockerfile. Current exception like:
# event-service  |   File "/app/app/infrastructure/db/migrations/env.py", line 5, in <module>
# event-service  |     import config
# event-service  | ModuleNotFoundError: No module named 'config'

app = create_app()
