import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from sensors_api.db.models.record import Record
from sensors_api.exceptions import DeviceNotFound
from sensors_api.schemas.records import RecordIn, RecordInResponse, RecordStatus

logger = logging.getLogger(__name__)


async def create_record(db_session: AsyncSession, record: RecordIn) -> RecordInResponse:
    record_obj = Record(**record.dict())
    db_session.add(record_obj)
    try:
        await db_session.commit()
    except IntegrityError as exc:
        raise DeviceNotFound(detail="Device not found") from exc
    return RecordInResponse(**record_obj.dict())


async def get_record_status_histogram(
    db_session: AsyncSession, device_id: str, limit: int, offset: int
) -> list[RecordStatus]:
    statement = select(Record).where(Record.device_id == device_id).limit(limit).offset(offset)
    result = await db_session.execute(statement)
    records = result.scalars()
    return [RecordStatus(status=record.status, timestamp=record.timestamp) for record in records]
