import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sensors_api.db.models.account import ClientAccount
from sensors_api.exceptions import InvalidCredentials
from sensors_api.helpers import generate_random_string, get_password_hash, verify_password
from sensors_api.schemas.accounts import AccountInResponse
from sensors_api.schemas.auth import AuthIn

logger = logging.getLogger(__name__)


async def create_client_account(db_session: AsyncSession, description: str) -> AccountInResponse:
    client_secret = generate_random_string()
    hashed_client_secret = get_password_hash(client_secret)
    client_account = ClientAccount(client_secret=hashed_client_secret, description=description)
    db_session.add(client_account)
    await db_session.commit()
    return AccountInResponse(
        client_id=client_account.client_id, client_secret=client_secret, description=description
    )


async def get_client_account_by_client_id(db_session: AsyncSession, client_id: str) -> ClientAccount:
    statement = select(ClientAccount).where(ClientAccount.client_id == client_id)
    result = await db_session.execute(statement)
    client_account = result.scalar()
    if not client_account:
        raise InvalidCredentials("Client Account not found.")
    if not client_account.active:
        raise InvalidCredentials("Client Account inactive.")
    return client_account


async def validate_credentials(db_session: AsyncSession, credentials: AuthIn) -> AccountInResponse:
    client_account = await get_client_account_by_client_id(db_session, credentials.client_id)
    if not verify_password(credentials.client_secret, client_account.client_secret):
        raise InvalidCredentials("Client Secret doesn't match.")
    return AccountInResponse(**client_account.dict())
