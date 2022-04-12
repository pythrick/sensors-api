from datetime import datetime, timedelta

import jwt

from config import settings

from sensors_api.schemas.auth import AuthIn, AuthInResponse


async def authenticate(account: AuthIn) -> AuthInResponse:
    access_token = jwt.encode(
        {
            "client_id": account.client_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.access_token_expiration_secs),
        },
        settings.api_secret,
        "HS256",
    )
    refresh_token = jwt.encode(
        {
            "client_id": account.client_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.refresh_token_expiration_secs),
        },
        settings.api_secret,
        "HS256",
    )
    return AuthInResponse(access_token=access_token, refresh_token=refresh_token)


async def refresh(client_id: str) -> str:
    return jwt.encode(
        {
            "client_id": client_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.access_token_expiration_secs),
        },
        settings.api_secret,
        "HS256",
    )


async def validate_token(token: str) -> str:
    result = jwt.decode(token, settings.api_secret, "HS256", options={"verify_exp": True})
    return result["client_id"]
