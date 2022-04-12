import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from sensors_api.api import app
from sensors_api.dependencies import get_session


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        "sqlite+aiosqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="client")
async def client_fixture(session: AsyncSession):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def record_dict():
    return {
        "deviceId": "sensor-1",
        "timestamp": "2022-04-11T23:06:55.256000",
        "status": "ON",
        "pressure": 212.0,
        "temperature": 200,
    }


@pytest.fixture
def device_dict():
    return {"interval": 5}


@pytest_asyncio.fixture
async def record(client: AsyncClient, record_dict: dict):
    return await client.post("/v1/records", json=record_dict)


@pytest_asyncio.fixture
async def device(client: AsyncClient, device_dict: dict):
    return await client.post("/v1/devices", json=device_dict)
