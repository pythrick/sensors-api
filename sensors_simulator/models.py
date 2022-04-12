from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from shared.helpers import to_camel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Device(BaseSchema):
    id: str
    interval: int


class Record(BaseSchema):
    id: str
    device_id: str
    timestamp: datetime
    status: str
    pressure: Decimal
    temperature: int
