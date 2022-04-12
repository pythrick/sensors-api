from fastapi import APIRouter, Depends
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from sensors_api.core import auth
from sensors_api.core.accounts import get_client_account_by_client_id, validate_credentials
from sensors_api.core.auth import validate_token
from sensors_api.dependencies import get_session
from sensors_api.exceptions import InvalidCredentials, InvalidToken, Unauthorized
from sensors_api.schemas.auth import AuthIn, AuthInResponse, RefreshIn, RefreshInResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/token", response_model=AuthInResponse)
async def authenticate(credentials: AuthIn, session: AsyncSession = Depends(get_session)) -> AuthInResponse:
    """Generate authentication tokens."""
    try:
        await validate_credentials(session, AuthIn(**credentials.dict()))
        response = await auth.authenticate(credentials)
    except InvalidCredentials as exc:
        raise Unauthorized("Invalid credentials") from exc
    return response


@auth_router.post("/refresh", response_model=RefreshInResponse)
async def refresh(data: RefreshIn, session: AsyncSession = Depends(get_session)) -> RefreshInResponse:
    """Refresh access_token."""
    try:
        client_id = await validate_token(data.refresh_token)
    except InvalidTokenError as exc:
        raise InvalidToken from exc
    client_account = await get_client_account_by_client_id(session, client_id)
    refreshed_access_token = await auth.refresh(client_account.client_id)
    return RefreshInResponse(access_token=refreshed_access_token, refresh_token=data.refresh_token)
