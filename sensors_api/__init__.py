from datetime import datetime

from fastapi import FastAPI, Depends

from sensors_api.dependencies import get_token_header
from sensors_api.routers import v1

app = FastAPI()

app.include_router(v1.router, prefix="/v1", dependencies=[Depends(get_token_header)])

started = datetime.utcnow()


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "OK"}
