import asyncio
import logging
import random
from http import HTTPStatus

from faker import Faker
from httpx import AsyncClient, ConnectError
from pydantic import BaseModel, Field

from sensors_simulator.exceptions import NoConnection
from sensors_simulator.models import Device, Record
from shared.enums import StatusEnum

logger = logging.getLogger(__name__)
fake = Faker()


class Simulator(BaseModel):
    base_url: str
    devices_num: int = Field(..., gt=9)
    streaming_interval: int | None = None

    async def start(
        self,
    ):
        async with AsyncClient(base_url=self.base_url) as client:
            await self._ping(client)
            records_tasks = []
            devices = await self._create_devices(client)
            for device in devices:
                records_tasks.append(asyncio.ensure_future(self._create_record(client, device)))
            await asyncio.gather(*records_tasks)

    @staticmethod
    async def _ping(client: AsyncClient):
        try:
            response = await client.get("/ping")
            if response.status_code != HTTPStatus.OK:
                raise NoConnection
        except ConnectError as e:
            raise NoConnection("Unable to connect to API.") from e

    async def _create_devices(self, client: AsyncClient):
        devices_tasks = []
        for _ in range(self.devices_num):
            devices_tasks.append(asyncio.ensure_future(self._create_device(client)))
        devices = await asyncio.gather(*devices_tasks)
        return devices

    async def _create_device(self, client: AsyncClient) -> Device:
        response = await client.post(
            "/v1/devices", json={"interval": self.streaming_interval or random.choice(range(2, 10))}
        )
        response.raise_for_status()
        device = Device(**response.json())
        logger.info(f"Device '{device.id}' registered with interval of {device.interval} secs.")
        return device

    @staticmethod
    async def _create_record(client, device: Device):
        counter = 1
        while True:
            response = await client.post(
                "/v1/records",
                json={
                    "deviceId": device.id,
                    "timestamp": fake.date_time().isoformat(),
                    "status": random.choice([s.value for s in StatusEnum]),
                    "pressure": fake.pyfloat(right_digits=3, positive=True),
                    "temperature": fake.pyint(),
                },
            )
            response.raise_for_status()
            record = Record(**response.json())
            logger.info(f"Device ID: {device.id}\tRecord ID: {record.id}\tCounter: {counter}")
            await asyncio.sleep(device.interval)
            counter += 1
