from fastapi import FastAPI, Depends

from sensors_api.dependencies import get_token_header
from sensors_api.routers import v1

app = FastAPI(
    title="Sensors API",
    contact={"name": "Patrick Rodrigues", "email": "patrick.pwall@gmail.com"},
    license_info={"name": "MIT"},
)

app.include_router(v1.router, prefix="/v1", dependencies=[Depends(get_token_header)])


@app.get("/healthcheck")
async def healthcheck():
    """Provides a simple API healthcheck"""
    return {"message": "OK"}
