from datetime import datetime
from decimal import Decimal

from sensors_api.enums import StatusEnum
from sensors_api.schemas.base_schema import BaseSchema


class RecordIn(BaseSchema):
    device_id: str
    timestamp: datetime
    status: StatusEnum
    pressure: Decimal
    temperature: int


class RecordInResponse(RecordIn):
    id: str


class RecordStatus(BaseSchema):
    timestamp: datetime
    status: StatusEnum
