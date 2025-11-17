from app.domain.models import Event
from app.infrastructure.db.tables import EventTable


class EventMapper:
    @staticmethod
    def domain_to_table(event):
        return EventTable(
            id=event.id,
            object_id=event.object_id,
            user_id=event.user_id,
            description=event.description,
            timestamp=event.timestamp
        )

    @staticmethod
    def table_to_domain(obj):
        return Event(
            id=obj.id,
            object_id=obj.object_id,
            user_id=obj.user_id,
            description=obj.description,
            timestamp=obj.timestamp
        )
