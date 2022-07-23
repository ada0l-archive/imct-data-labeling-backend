from backend.core.settings.app_env_types import AppEnvTypes
from backend.core.settings.app_settings import (
    AppSettings,
    DevAppSettings,
    HerokuAppSettings,
    ProdAppSettings,
    TestAppSettings,
)
from backend.core.settings.base_app_settings import BaseAppSettings

environments: dict[AppEnvTypes, type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
    AppEnvTypes.heroku: HerokuAppSettings,
}

app_env = BaseAppSettings().app_env
settings = environments[app_env]()  # type: ignore
