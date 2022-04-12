import logging

from fastapi import FastAPI

from sensors_api.api.v1 import v1_router
from sensors_api.db.connection import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sensors API",
    contact={"name": "Patrick Rodrigues", "email": "patrick.pwall@gmail.com"},
    license_info={"name": "MIT"},
)

app.include_router(v1_router)


@app.on_event("startup")
async def on_startup():
    from sensors_api.db.models.device import Device  # noqa
    from sensors_api.db.models.record import Record  # noqa

    logger.info("Initializing database...")
    await init_db()


@app.get("/ping")
async def ping():
    """Provide a simple API healthcheck."""
    return {"ping": "pong!"}
