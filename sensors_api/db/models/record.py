from datetime import datetime
from decimal import Decimal

from sqlmodel import Field

from .base_model import BaseModel


class Record(BaseModel, table=True):
    __tablename__: str = "records"

    device_id: str = Field(..., foreign_key="devices.id")
    timestamp: datetime
    status: str
    pressure: Decimal
    temperature: int
