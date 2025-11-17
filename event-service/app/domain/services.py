from app.domain.models import Event
from app.infrastructure.db.repositories import EventRepository


class EventService:
    def __init__(self, session):
        self.repo = EventRepository(session)

    async def create_event(self, dto, user_id):
        event = Event(
            object_id=dto.object_id,
            user_id=user_id,
            description=dto.description,
            timestamp=dto.timestamp,
        )

        saved = await self.repo.save(event)
        return saved
