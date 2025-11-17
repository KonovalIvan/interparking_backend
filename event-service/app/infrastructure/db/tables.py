from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class EventTable(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    object_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
