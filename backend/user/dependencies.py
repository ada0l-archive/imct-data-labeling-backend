from fastapi import Depends
from fastapi_azure_auth.user import User as UserAzureLib

from backend.user.schemas import (
    azure_scheme,
    azure_scheme_without_error,
    UserAzure
)


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

