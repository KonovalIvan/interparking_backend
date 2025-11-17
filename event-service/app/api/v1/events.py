from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_db_session
from app.application.dto.event_dto import EventCreateDTO
from app.domain.services import EventService

router = APIRouter()


@router.post("/")
async def create_event(
        dto: EventCreateDTO,
        user=Depends(get_current_user),
        session=Depends(get_db_session)
):
    service = EventService(session)
    event = await service.create_event(dto, user_id=user["sub"])
    return {"status": "ok", "event": event.__dict__}
