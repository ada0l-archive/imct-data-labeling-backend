from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from backend.core.settings import settings
from backend.handlers import shutdown_handler, startup_handler


def get_application():
    _app = FastAPI(**settings.fastapi_kwargs)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.backend_cors_origins
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router_v1 = APIRouter(prefix="/v1")
    _app.include_router(router_v1)

    _app.add_event_handler("startup", startup_handler)
    _app.add_event_handler("shutdown", shutdown_handler)

    return _app


app = get_application()
