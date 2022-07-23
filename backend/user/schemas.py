from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from pydantic import BaseModel

from backend.core.settings import settings

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.app_client_id,
    tenant_id=settings.tenant_id,
    scopes={
        f'api://{settings.app_client_id}/user_impersonation': 'user_impersonation',
    }
)

azure_scheme_without_error = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.app_client_id,
    tenant_id=settings.tenant_id,
    scopes={
        f'api://{settings.app_client_id}/user_impersonation': 'user_impersonation',
    },
    auto_error=False
)


class UserAzure(BaseModel):
    full_name: str
    email: str


class UserBasePydantic(BaseModel):
    email: str
    full_name: str


class UserPydantic(UserBasePydantic):
    id: int

    class Config:
        orm_mode = True


class UserInCreatePydantic(UserBasePydantic):
    pass


class UserInUpdatePydantic(UserBasePydantic):
    pass
