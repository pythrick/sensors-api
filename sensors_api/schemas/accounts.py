from sensors_api.schemas.base_schema import BaseSchema


class AccountIn(BaseSchema):
    description: str


class AccountInResponse(AccountIn):
    client_id: str
    client_secret: str
