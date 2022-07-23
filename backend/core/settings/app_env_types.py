from enum import Enum


class AppEnvTypes(Enum):
    prod = "prod"
    dev = "dev"
    test = "test"
    heroku = "heroku"
