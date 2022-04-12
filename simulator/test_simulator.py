import asyncio
import logging
import random

from faker import Faker
from httpx import AsyncClient

from config import settings

from sensors_api.enums import StatusEnum

logger = logging.getLogger(__name__)

fake = Faker()


def generate_record(device_id: str):
    return {
        "deviceId": device_id,
        "timestamp": fake.date_time().isoformat(),
        "status": random.choice([s.value for s in StatusEnum]),
        "pressure": fake.pyfloat(right_digits=3, positive=True),
        "temperature": fake.pyint(),
    }


def generate_device(streaming_interval: int = None):
    """Generate a fake device."""
    return {"interval": streaming_interval or random.choice(range(2, 10))}


async def create_record(client: AsyncClient, device_id: str, interval: int):
    counter = 1
    while True:
        response = await client.post("/v1/records", json=generate_record(device_id))
        response.raise_for_status()
        record_data = response.json()
        logger.info(f"Device ID: {device_id}\tRecord ID: {record_data['id']}\tCounter: {counter}")
        await asyncio.sleep(interval)
        counter += 1


async def create_device(client: AsyncClient, streaming_interval: int = None):
    return await client.post("/v1/devices", json=generate_device(streaming_interval))


async def authenticate(client: AsyncClient, client_account: AccountInResponse):
    response = await client.post("/v1/auth/token", json=AuthIn(**client_account.dict()).dict())
    response.raise_for_status()
    data = response.json()
    client.headers.update({"Authorization": f"Bearer {data['accessToken']}"})


async def start_simulator(devices_num: int, streaming_interval: int = None):
    async with AsyncClient(base_url=settings.base_url) as client:
        client_account = await create_client_account(description="Simulator Account")
        await authenticate(client, client_account)
        devices_tasks = []
        for _ in range(devices_num):
            devices_tasks.append(asyncio.ensure_future(create_device(client, streaming_interval)))
        devices_responses = await asyncio.gather(*devices_tasks)

        records_tasks = []
        for device_response in devices_responses:
            device_data = device_response.json()
            device_id = device_data["id"]
            device_interval = device_data["interval"]
            logger.info(f"Device '{device_id}' registered will stream every of '{device_interval}' secs.")

            records_tasks.append(asyncio.ensure_future(create_record(client, device_id, device_interval)))

        await asyncio.gather(*records_tasks)
