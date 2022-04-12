from sqlmodel import Field

from ...helpers import generate_uuid
from .base_model import BaseModel


class ClientAccount(BaseModel, table=True):
    __tablename__: str = "client_accounts"

    description: str
    client_id: str = Field(default_factory=generate_uuid)
    client_secret: str
    active: bool = True
