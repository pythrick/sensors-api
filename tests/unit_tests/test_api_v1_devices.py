import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_api_v1_devices_create(device, device_dict):
    assert device.status_code == status.HTTP_201_CREATED
    response_data = device.json()
    device_id = response_data.pop("id")
    assert device_id
    assert isinstance(device_id, str)
    assert response_data == device_dict
