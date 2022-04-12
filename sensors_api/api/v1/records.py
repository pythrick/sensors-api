from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings

from sensors_api.core.records import create_record, get_record_status_histogram
from sensors_api.dependencies import get_session
from sensors_api.schemas.records import RecordIn, RecordInResponse, RecordStatus

records_router = APIRouter(prefix="/records", tags=["Records"])


@records_router.post(
    "",
    response_model=RecordInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(record: RecordIn, session: AsyncSession = Depends(get_session)) -> RecordInResponse:
    """Store device records."""
    return await create_record(session, record)


@records_router.get("/status-histogram", response_model=list[RecordStatus])
async def get_status_histogram(
    device_id: str = Query(..., alias="deviceId"),
    limit: int | None = Query(default=settings.pagination_limit),
    offset: int | None = Query(default=0),
    session: AsyncSession = Depends(get_session),
):
    """Get device histogram."""
    return await get_record_status_histogram(session, device_id, limit, offset)
