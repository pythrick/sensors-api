from sensors_api.schemas.base_schema import BaseSchema


class AuthIn(BaseSchema):
    client_id: str
    client_secret: str


class AuthInResponse(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshIn(BaseSchema):
    refresh_token: str


class RefreshInResponse(AuthInResponse):
    ...
