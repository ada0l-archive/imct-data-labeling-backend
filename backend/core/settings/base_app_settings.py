from pydantic import BaseSettings

from backend.core.settings.app_env_types import AppEnvTypes


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.heroku

    class Config:
        pass
