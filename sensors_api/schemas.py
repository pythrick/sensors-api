from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, fields

from sensors_api.helpers import to_camel, uuid_generator


class StatusEnum(str, Enum):
    ON = "ON"
    OFF = "OFF"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class RecordIn(BaseSchema):
    device_id: str
    timestamp: datetime
    status: StatusEnum
    pressure: Decimal
    temperature: int


class RecordInResponse(RecordIn):
    record_id: str = fields.Field(default_factory=uuid_generator)


class DeviceIn(BaseSchema):
    device_id: str | None = fields.Field(default_factory=uuid_generator)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class DeviceInResponse(DeviceIn):
    api_token: str
    created_at: datetime = fields.Field(default_factory=datetime.utcnow, init=False)


class Device(DeviceIn):
    histogram: list[RecordIn] = fields.Field(default_factory=list)


class AuthIn(BaseSchema):
    device_id: str
    api_key: str


class AuthInResponse(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshIn(BaseSchema):
    refresh_token: str


class RefreshInResponse(AuthInResponse):
    ...
