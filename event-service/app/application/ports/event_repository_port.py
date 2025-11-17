from asyncio import Protocol, Event
from uuid import UUID


class EventRepositoryPort(Protocol):
    async def save(self, event: Event) -> Event: ...

    async def get_by_id(self, event_id: UUID) -> Event: ...

    async def list_for_object(self, object_id: UUID) -> list[Event]: ...
