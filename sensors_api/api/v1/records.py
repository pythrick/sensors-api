from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared.enums import ParameterEnum

from sensors_api.core.records import create_record, get_record_status_histogram, get_the_top_values
from sensors_api.dependencies import get_session
from sensors_api.schemas.records import RecordIn, RecordInResponse

records_router = APIRouter(prefix="/records", tags=["Records"])


@records_router.post(
    "",
    response_model=RecordInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(record: RecordIn, session: AsyncSession = Depends(get_session)) -> RecordInResponse:
    """Store device records."""
    return await create_record(session, record)


@records_router.get("/status-histogram")
async def get_status_histogram(
    device_id: str = Query(..., alias="deviceId"),
    session: AsyncSession = Depends(get_session),
):
    """Get device histogram."""
    return await get_record_status_histogram(session, device_id)


@records_router.get("/top-values")
async def get_top_values(
    parameter: ParameterEnum,
    records_number: int,
    session: AsyncSession = Depends(get_session),
):
    result = await get_the_top_values(session, parameter, records_number)
    return result
