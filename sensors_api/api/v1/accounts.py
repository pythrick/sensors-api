from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from sensors_api.core.accounts import create_client_account
from sensors_api.dependencies import get_session
from sensors_api.schemas.accounts import AccountIn, AccountInResponse

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@accounts_router.post(
    "",
    response_model=AccountInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(account: AccountIn, session: AsyncSession = Depends(get_session)) -> AccountInResponse:
    """Create new Sensors API client account."""
    return await create_client_account(session, account.description)
