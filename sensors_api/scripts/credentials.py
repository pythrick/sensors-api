from sensors_api.core import accounts as accounts_core
from sensors_api.dependencies import get_session
from sensors_api.schemas.accounts import AccountInResponse
from sensors_api.schemas.auth import AuthIn


async def create_client_account(description: str) -> AccountInResponse:
    async for session in get_session():
        return await accounts_core.create_client_account(session, description)


async def validate_credentials(client_id: str, client_secret: str) -> AccountInResponse:
    async for session in get_session():
        return await accounts_core.validate_credentials(
            session, AuthIn(client_id=client_id, client_secret=client_secret)
        )
