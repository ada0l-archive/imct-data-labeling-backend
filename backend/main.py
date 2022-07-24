from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from backend.core.settings import settings
from backend.handlers import shutdown_handler, startup_handler
from backend.user.api.v1 import router as user_router_v1
from backend.user.api.v1 import me_router as me_user_router_v1
from backend.project.api.v1 import router as project_router_v1

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
    router_v1.include_router(user_router_v1, prefix="/user", tags=["user"])
    router_v1.include_router(me_user_router_v1, prefix="/me", tags=["me"])
    router_v1.include_router(project_router_v1,
                             prefix="/project", tags=["project"])
    _app.include_router(router_v1)

    _app.add_event_handler("startup", startup_handler)
    _app.add_event_handler("shutdown", shutdown_handler)

    return _app


app = get_application()
