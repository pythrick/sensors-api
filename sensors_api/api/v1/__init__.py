from fastapi import APIRouter

from sensors_api.api.v1.auth import auth_router
from sensors_api.api.v1.devices import devices_router
from sensors_api.api.v1.records import records_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(records_router)
v1_router.include_router(devices_router)
