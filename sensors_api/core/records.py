import logging
from collections import defaultdict

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from shared.enums import ParameterEnum, StatusEnum

from sensors_api.db.models.record import Record
from sensors_api.exceptions import DeviceNotFound
from sensors_api.schemas.records import RecordIn, RecordInResponse

logger = logging.getLogger(__name__)


async def create_record(db_session: AsyncSession, record: RecordIn) -> RecordInResponse:
    record_obj = Record(**record.dict())
    db_session.add(record_obj)
    try:
        await db_session.commit()
    except IntegrityError as exc:
        raise DeviceNotFound(detail="Device not found") from exc
    return RecordInResponse(**record_obj.dict())


async def get_record_status_histogram(db_session: AsyncSession, device_id: str) -> dict:
    statement = select(Record).where(Record.device_id == device_id)
    result = await db_session.execute(statement)
    records = result.scalars()

    status_counter = defaultdict(int)
    for status in StatusEnum:
        status_counter[status.value] = 0
    for record in records:
        status_counter[record.status] += 1
    return status_counter


async def get_the_top_values(db_session: AsyncSession, parameter: ParameterEnum, records_number: int):
    field = getattr(Record, parameter.value)
    statement = select(Record).order_by(desc(field)).limit(records_number)
    result = await db_session.execute(statement)
    records = result.scalars()
    return list(records)
