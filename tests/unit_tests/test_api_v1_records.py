import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_api_v1_records_create(record, record_dict):
    assert record.status_code == status.HTTP_201_CREATED
    response_data = record.json()
    record_id = response_data.pop("id")
    assert record_id
    assert isinstance(record_id, str)
    assert response_data == record_dict


@pytest.mark.asyncio
async def test_api_v1_records_get_status_histogram(record, client):
    record_data = record.json()
    device_id = record_data["deviceId"]
    response = await client.get(f"/v1/records/status-histogram?deviceId={device_id}")
    response_data = response.json()
    assert response_data == {"ACTIVE": 0, "INACTIVE": 0, "OFF": 0, "ON": 1}
