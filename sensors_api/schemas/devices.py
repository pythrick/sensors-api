from sensors_api.schemas.base_schema import BaseSchema


class DeviceIn(BaseSchema):
    interval: int


class DeviceInResponse(DeviceIn):
    id: str
