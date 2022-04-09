from fastapi import APIRouter, status, Path

from sensors_api.helpers import api_key_generator
from sensors_api.schemas import (
    DeviceIn,
    RecordIn,
    DeviceInResponse,
    Device,
    RecordInResponse,
    AuthInResponse,
    AuthIn,
    RefreshInResponse,
)

router = APIRouter()


@router.post("/auth", tags=["Authentication"], response_model=AuthInResponse)
async def authenticate(auth: AuthIn) -> AuthInResponse:
    """Generate authentication tokens."""
    return AuthInResponse(access_token="xxx", refresh_token="yyy")


@router.get("/refresh", tags=["Authentication"], response_model=RefreshInResponse)
async def refresh() -> RefreshInResponse:
    """Refresh access_token."""
    return RefreshInResponse(access_token="xxx+1", refresh_token="yyy")


@router.post(
    "/devices",
    tags=["devices"],
    response_model=DeviceInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_device(device: DeviceIn) -> DeviceInResponse:
    """Register device to store records."""
    # TODO: Implement it
    return DeviceInResponse(api_token=api_key_generator(), **device.dict())


@router.get("/devices/{deviceId}", tags=["devices"], response_model=Device)
async def get_device_histogram(
    device_id: str = Path(default=..., alias="deviceId")
) -> Device:
    """Provides device histogram."""
    # TODO: Implement it
    return Device(histogram=[])


@router.post(
    "/records",
    tags=["records"],
    response_model=RecordInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_record(record: RecordIn) -> RecordInResponse:
    """Store device records."""
    # TODO: Implement it
    return RecordInResponse(**record.dict())
