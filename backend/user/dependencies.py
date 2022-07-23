from fastapi import Depends, HTTPException, status
from fastapi_azure_auth.user import User as UserAzureLib
from backend.core.database import get_session
from backend.user.models import User
from backend.user.repository import UserRepository

from backend.user.schemas import (
    azure_scheme,
    azure_scheme_without_error,
    UserAzure
)


def get_user_rep(session=Depends(get_session)):
    return UserRepository(session)

def get_user_azure(
    user_azure: UserAzureLib = Depends(azure_scheme)
) -> UserAzure:
    return UserAzure(
        email=user_azure.claims["preferred_username"],
        full_name=user_azure.claims["name"],
    )


def get_user_azure_without_error(
    user_azure: UserAzureLib = Depends(azure_scheme_without_error)
) -> UserAzure | None:
    if user_azure:
        return UserAzure(
            email=user_azure.claims["preferred_username"],
            full_name=user_azure.claims["name"],
        )
    return None


async def get_current_user(
    user_rep: UserRepository = Depends(get_user_rep),
    azure_user: UserAzure = Depends(get_user_azure)
) -> User:
    if azure_user:
        user = await user_rep.get_by_email(azure_user.email)
        if user:
            return user
    raise HTTPException(
        detail="The user is not exist",
        status_code=status.HTTP_403_FORBIDDEN,
    )
