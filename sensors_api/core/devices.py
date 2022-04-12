import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sensors_api.db.models.device import Device
from sensors_api.schemas.devices import DeviceIn, DeviceInResponse

logger = logging.getLogger(__name__)


async def create_device(db_session: AsyncSession, device: DeviceIn) -> DeviceInResponse:
    device_obj = Device(**device.dict())
    db_session.add(device_obj)
    await db_session.commit()
    return DeviceInResponse(**device_obj.dict())
