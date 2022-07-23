from fastapi import APIRouter, Depends, HTTPException, status

from backend.core.database import get_session
from backend.invite.repository import InviteRepository
from backend.user.dependencies import get_user_azure
from backend.user.repository import UserRepository
from backend.user.schemas import UserAzure, UserPydantic

router = APIRouter()


def get_user_rep(session=Depends(get_session)):
    return UserRepository(session)


def get_invite_rep(session=Depends(get_session)):
    return InviteRepository(session)


@router.post("/", response_model=UserPydantic)
async def create_user(
    user_rep: UserRepository = Depends(get_user_rep),
    invite_rep: InviteRepository = Depends(get_invite_rep),
    user: UserAzure = Depends(get_user_azure)
):
    invite = await invite_rep.get_by_email(user.email)
    if not invite:
        raise HTTPException(
            detail="You weren't invited",
            status_code=status.HTTP_409_FORBIDDEN
        )
    user_in_db = await user_rep.get_by_email(user.email)
    if user_in_db:
        raise HTTPException(
            detail="This email is already taken",
            status_code=status.HTTP_409_CONFLICT
        )
    return await user_rep.create(user)
