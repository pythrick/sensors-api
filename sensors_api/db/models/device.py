from .base_model import BaseModel


class Device(BaseModel, table=True):
    __tablename__: str = "devices"

    interval: int  # Interval in seconds to post data
