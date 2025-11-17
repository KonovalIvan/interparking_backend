from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EventCreateDTO(BaseModel):
    object_id: UUID
    description: str
    timestamp: datetime
