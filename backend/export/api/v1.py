from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_export():
    return "export app created!"
