from app.infrastructure.db.tables import EventTable
from app.infrastructure.mappers.event_mapper import EventMapper
from sqlalchemy import select


class EventRepository:
    def __init__(self, session):
        self.session = session

    async def save(self, event):
        table_obj = EventMapper.domain_to_table(event)
        self.session.add(table_obj)
        await self.session.commit()
        return EventMapper.table_to_domain(table_obj)

    async def get(self, id):
        stmt = select(EventTable).where(EventTable.id == id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        return EventMapper.table_to_domain(obj) if obj else None
