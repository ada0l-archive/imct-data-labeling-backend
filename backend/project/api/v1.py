from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_project():
    return "project app created!"
