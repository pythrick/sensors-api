from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from sensors_api.core.devices import create_device
from sensors_api.dependencies import get_session
from sensors_api.schemas.devices import DeviceIn, DeviceInResponse

devices_router = APIRouter(prefix="/devices", tags=["Devices"])


@devices_router.post(
    "",
    response_model=DeviceInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(device: DeviceIn, session: AsyncSession = Depends(get_session)) -> DeviceInResponse:
    """Create new streaming device."""
    return await create_device(session, device)
