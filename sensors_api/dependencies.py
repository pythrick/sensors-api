from typing import AsyncGenerator

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from sensors_api.core.accounts import get_client_account_by_client_id
from sensors_api.core.auth import validate_token
from sensors_api.db.connection import engine
from sensors_api.exceptions import InvalidToken


async def get_session() -> AsyncGenerator[AsyncSession, AsyncSession]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_token_header(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if not credentials:
        raise InvalidToken
    try:
        await validate_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise InvalidToken from exc
    return True


async def get_current_account(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: AsyncSession = Depends(get_session),
):
    client_id = await validate_token(credentials.credentials)
    client_account = await get_client_account_by_client_id(session, client_id)
    return client_account
