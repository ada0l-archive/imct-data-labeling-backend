from fastapi import APIRouter, Depends, HTTPException, status

from backend.invite.dependencies import get_invite_rep
from backend.invite.repository import InviteRepository
from backend.user.dependencies import get_current_user, get_user_azure
from backend.user.models import User
from backend.user.repository import UserRepository
from backend.user.schemas import UserAzure, UserPydantic

router = APIRouter()


@router.post("/", response_model=UserPydantic)
async def create_user(
    user_rep: UserRepository = Depends(get_user_azure),
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

me_router = APIRouter()


@me_router.get("/", response_model=UserPydantic)
async def get_me(
    user: User = Depends(get_current_user)
):
    return user
